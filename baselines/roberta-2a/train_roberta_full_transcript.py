"""
RoBERTa Full-Transcript Baseline Training Script

Trains RoBERTa-base for static binary fraud classification on full transcripts.
"""

import json
import os
import time
from pathlib import Path
from datetime import timedelta
from typing import List, Dict, Tuple
import numpy as np
import torch
from torch.utils.data import Dataset, DataLoader
from transformers import (
    RobertaTokenizer, 
    RobertaForSequenceClassification,
    get_linear_schedule_with_warmup,
    TrainingArguments,
    Trainer,
    EarlyStoppingCallback
)
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score, 
    precision_recall_fscore_support,
    classification_report,
    confusion_matrix
)
from tqdm.auto import tqdm
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

# Set random seeds for reproducibility
SEED = 42
torch.manual_seed(SEED)
np.random.seed(SEED)

# Configuration
class Config:
    # Paths
    DATA_ROOT = Path("../../output/source_conversations")
    OUTPUT_DIR = Path("../../baseline/roberta-2a/models")
    RESULTS_DIR = Path("../../baseline/roberta-2a/results")
    
    # Model settings
    MODEL_NAME = "roberta-base"
    MAX_LENGTH = 512
    
    # Training settings
    BATCH_SIZE = 4  # Reduced for M4 GPU memory (was 16)
    GRADIENT_ACCUMULATION_STEPS = 4  # Effective batch size = 4 * 4 = 16
    LEARNING_RATE = 2e-5
    NUM_EPOCHS = 5
    WARMUP_RATIO = 0.1
    WEIGHT_DECAY = 0.01
    
    # Data split
    TEST_SIZE = 0.15
    VAL_SIZE = 0.15
    
    # Device
    DEVICE = "mps" if torch.backends.mps.is_available() else "cpu"
    
    # Logging
    LOGGING_STEPS = 50
    EVAL_STEPS = 500
    SAVE_STEPS = 500
    SAVE_TOTAL_LIMIT = 3

# Create output directories
Config.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
Config.RESULTS_DIR.mkdir(parents=True, exist_ok=True)

print(f"Starting RoBERTa Full-Transcript Training")
print(f"Device: {Config.DEVICE}")
print(f"Model: {Config.MODEL_NAME}")
print(f"Batch size: {Config.BATCH_SIZE} (effective: {Config.BATCH_SIZE * Config.GRADIENT_ACCUMULATION_STEPS} with gradient accumulation)")
print(f"Epochs: {Config.NUM_EPOCHS}")
print("="*70)


class FraudDataset(Dataset):
    """Custom Dataset for fraud detection conversations"""
    
    def __init__(self, texts: List[str], labels: List[int], tokenizer, max_length: int):
        self.texts = texts
        self.labels = labels
        self.tokenizer = tokenizer
        self.max_length = max_length
    
    def __len__(self):
        return len(self.texts)
    
    def __getitem__(self, idx):
        text = self.texts[idx]
        label = self.labels[idx]
        
        encoding = self.tokenizer(
            text,
            add_special_tokens=True,
            max_length=self.max_length,
            padding='max_length',
            truncation=True,
            return_tensors='pt'
        )
        
        return {
            'input_ids': encoding['input_ids'].flatten(),
            'attention_mask': encoding['attention_mask'].flatten(),
            'labels': torch.tensor(label, dtype=torch.long)
        }


def load_conversation_data() -> Tuple[List[str], List[int], List[Dict]]:
    """
    Load all conversations from batch folders
    Returns: (texts, labels, metadata)
    """
    print("\nLoading conversations from all batch folders...")
    
    texts = []
    labels = []
    metadata = []
    
    # Get all batch folders
    batch_folders = sorted([
        d for d in Config.DATA_ROOT.iterdir() 
        if d.is_dir() and d.name.startswith('batch_')
    ])
    
    print(f"Found {len(batch_folders)} batch folders")
    
    total_files = 0
    for batch_folder in tqdm(batch_folders, desc="Loading batches"):
        json_files = list(batch_folder.glob("*.json"))
        
        for json_file in tqdm(json_files, desc=f"  {batch_folder.name}", leave=False):
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Extract full transcript text
                transcript_parts = []
                for turn in data.get('transcript', []):
                    speaker = turn.get('speaker', 'Unknown')
                    text = turn.get('text', '')
                    transcript_parts.append(f"{speaker}: {text}")
                
                full_text = " ".join(transcript_parts)
                
                # Extract label
                final_verdict = data.get('final_verdict', 'NO')
                label = 1 if final_verdict == 'YES' else 0
                
                texts.append(full_text)
                labels.append(label)
                metadata.append({
                    'file': json_file.name,
                    'batch': batch_folder.name,
                    'session_id': data.get('session_id'),
                    'scenario_id': data.get('scenario', {}).get('scenario_id'),
                    'case_type': data.get('scenario', {}).get('case_type'),
                    'scam_outcome': data.get('scam_outcome')
                })
                
                total_files += 1
                
            except Exception as e:
                print(f"\n Error loading {json_file}: {e}")
                continue
    
    print(f"\nLoaded {total_files} conversations")
    print(f"   - Fraud cases (YES): {sum(labels)}")
    print(f"   - Non-fraud cases (NO): {len(labels) - sum(labels)}")
    print(f"   - Class balance: {sum(labels)/len(labels)*100:.1f}% fraud")
    
    return texts, labels, metadata


def create_data_splits(texts: List[str], labels: List[int], metadata: List[Dict]):
    """Split data into train/val/test sets"""
    print("\nCreating data splits...")
    
    # First split: separate test set
    train_val_texts, test_texts, train_val_labels, test_labels, train_val_meta, test_meta = \
        train_test_split(
            texts, labels, metadata,
            test_size=Config.TEST_SIZE,
            random_state=SEED,
            stratify=labels
        )
    
    # Second split: separate validation from training
    train_texts, val_texts, train_labels, val_labels, train_meta, val_meta = \
        train_test_split(
            train_val_texts, train_val_labels, train_val_meta,
            test_size=Config.VAL_SIZE / (1 - Config.TEST_SIZE),
            random_state=SEED,
            stratify=train_val_labels
        )
    
    print(f"   - Training set: {len(train_texts)} samples")
    print(f"   - Validation set: {len(val_texts)} samples")
    print(f"   - Test set: {len(test_texts)} samples")
    
    # Save metadata
    splits_info = {
        'train': {'size': len(train_texts), 'fraud': sum(train_labels), 'metadata': train_meta},
        'val': {'size': len(val_texts), 'fraud': sum(val_labels), 'metadata': val_meta},
        'test': {'size': len(test_texts), 'fraud': sum(test_labels), 'metadata': test_meta}
    }
    
    with open(Config.RESULTS_DIR / 'data_splits.json', 'w') as f:
        json.dump(splits_info, f, indent=2)
    
    return (train_texts, train_labels), (val_texts, val_labels), (test_texts, test_labels)


def compute_metrics(pred):
    """Compute metrics for evaluation"""
    labels = pred.label_ids
    preds = pred.predictions.argmax(-1)
    
    precision, recall, f1, _ = precision_recall_fscore_support(
        labels, preds, average='binary'
    )
    acc = accuracy_score(labels, preds)
    
    return {
        'accuracy': acc,
        'f1': f1,
        'precision': precision,
        'recall': recall
    }


def train_model(train_dataset, val_dataset):
    """Train RoBERTa model"""
    print("\nInitializing model and training...")
    
    # Load tokenizer and model
    tokenizer = RobertaTokenizer.from_pretrained(Config.MODEL_NAME)
    model = RobertaForSequenceClassification.from_pretrained(
        Config.MODEL_NAME,
        num_labels=2
    )
    
    # Training arguments
    training_args = TrainingArguments(
        output_dir=str(Config.OUTPUT_DIR),
        num_train_epochs=Config.NUM_EPOCHS,
        per_device_train_batch_size=Config.BATCH_SIZE,
        per_device_eval_batch_size=Config.BATCH_SIZE,
        gradient_accumulation_steps=Config.GRADIENT_ACCUMULATION_STEPS,  # Effective batch size = 16
        learning_rate=Config.LEARNING_RATE,
        weight_decay=Config.WEIGHT_DECAY,
        warmup_ratio=Config.WARMUP_RATIO,
        logging_dir=str(Config.OUTPUT_DIR / 'logs'),
        logging_steps=Config.LOGGING_STEPS,
        eval_strategy="steps",
        eval_steps=Config.EVAL_STEPS,
        save_steps=Config.SAVE_STEPS,
        save_total_limit=Config.SAVE_TOTAL_LIMIT,
        load_best_model_at_end=True,
        metric_for_best_model="f1",
        greater_is_better=True,
        fp16=False,  # MPS doesn't support fp16 yet
        dataloader_num_workers=0,  # MPS works best with 0 workers
        report_to="none",  # Disable wandb/tensorboard
        seed=SEED,
    )
    
    # Initialize Trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=val_dataset,
        compute_metrics=compute_metrics,
        callbacks=[EarlyStoppingCallback(early_stopping_patience=3)]
    )
    
    # Train
    print("\nStarting training...")
    start_time = time.time()
    
    train_result = trainer.train()
    
    training_time = time.time() - start_time
    print(f"\nTraining completed in {timedelta(seconds=int(training_time))}")
    
    # Save final model
    trainer.save_model(str(Config.OUTPUT_DIR / 'final_model'))
    tokenizer.save_pretrained(str(Config.OUTPUT_DIR / 'final_model'))
    
    return trainer, model, tokenizer


def evaluate_model(trainer, test_dataset, test_labels):
    """Evaluate model on test set"""
    print("\nEvaluating on test set...")
    
    # Get predictions
    predictions = trainer.predict(test_dataset)
    preds = predictions.predictions.argmax(-1)
    
    # Compute metrics
    accuracy = accuracy_score(test_labels, preds)
    precision, recall, f1, _ = precision_recall_fscore_support(
        test_labels, preds, average='binary'
    )
    
    # Detailed metrics
    class_report = classification_report(
        test_labels, preds,
        target_names=['Non-Fraud (NO)', 'Fraud (YES)'],
        digits=4
    )
    
    conf_matrix = confusion_matrix(test_labels, preds)
    
    # Print results
    print("\n" + "="*70)
    print("TEST SET RESULTS")
    print("="*70)
    print(f"Accuracy:  {accuracy:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall:    {recall:.4f}")
    print(f"F1-Score:  {f1:.4f}")
    print("\n" + class_report)
    print("\nConfusion Matrix:")
    print(f"                Predicted NO  Predicted YES")
    print(f"Actual NO       {conf_matrix[0][0]:12d}  {conf_matrix[0][1]:13d}")
    print(f"Actual YES      {conf_matrix[1][0]:12d}  {conf_matrix[1][1]:13d}")
    print("="*70)
    
    # Save results
    results = {
        'test_metrics': {
            'accuracy': float(accuracy),
            'precision': float(precision),
            'recall': float(recall),
            'f1_score': float(f1)
        },
        'classification_report': class_report,
        'confusion_matrix': conf_matrix.tolist(),
        'predictions': preds.tolist(),
        'true_labels': test_labels
    }
    
    with open(Config.RESULTS_DIR / 'test_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    # Save detailed results to CSV
    results_df = pd.DataFrame({
        'true_label': test_labels,
        'predicted_label': preds,
        'correct': [t == p for t, p in zip(test_labels, preds)]
    })
    results_df.to_csv(Config.RESULTS_DIR / 'predictions.csv', index=False)
    
    print(f"\nResults saved to {Config.RESULTS_DIR}")
    
    return results


def main():
    """Main training pipeline"""
    start_time = time.time()
    
    # Step 1: Load data
    texts, labels, metadata = load_conversation_data()
    
    # Step 2: Create splits
    (train_texts, train_labels), (val_texts, val_labels), (test_texts, test_labels) = \
        create_data_splits(texts, labels, metadata)
    
    # Step 3: Initialize tokenizer
    print("\nInitializing tokenizer...")
    tokenizer = RobertaTokenizer.from_pretrained(Config.MODEL_NAME)
    
    # Step 4: Create datasets
    print("Creating datasets...")
    train_dataset = FraudDataset(train_texts, train_labels, tokenizer, Config.MAX_LENGTH)
    val_dataset = FraudDataset(val_texts, val_labels, tokenizer, Config.MAX_LENGTH)
    test_dataset = FraudDataset(test_texts, test_labels, tokenizer, Config.MAX_LENGTH)
    
    # Step 5: Train model
    trainer, model, tokenizer = train_model(train_dataset, val_dataset)
    
    # Step 6: Evaluate on test set
    results = evaluate_model(trainer, test_dataset, test_labels)
    
    # Summary
    total_time = time.time() - start_time
    print("\n" + "="*70)
    print("TRAINING PIPELINE COMPLETED")
    print("="*70)
    print(f"Total time: {timedelta(seconds=int(total_time))}")
    print(f"Model saved to: {Config.OUTPUT_DIR / 'final_model'}")
    print(f"Results saved to: {Config.RESULTS_DIR}")
    print(f"Test F1-Score: {results['test_metrics']['f1_score']:.4f}")
    print("="*70)


if __name__ == "__main__":
    main()
