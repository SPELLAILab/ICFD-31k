# RoBERTa-2a: Full-Context Classification

Fine-tuned RoBERTa-base for fraud detection on complete conversation transcripts.

## Approach

- **Architecture**: RoBERTa-base (125M parameters)
- **Input**: Full conversation transcript (all turns concatenated)
- **Task**: Binary classification (fraud vs. legitimate)
- **Training**: Supervised fine-tuning on 24,800 conversations

## Files

### Training
- `train_roberta_full_transcript.py` - Main training script
- `requirements_training.txt` - Training dependencies

### Testing
- `test_roberta_2a_model.py` - Main test set evaluation
- `test_full_dataset.py` - Full dataset evaluation
- `test_kfold_validation.py` - K-fold cross-validation
- `test_cross_domain.py` - Generalization to unseen fraud types

## Results

### Main Test Set (`test_results/`)
- **Accuracy**: 99.62%
- **Precision**: 99.44%
- **Recall**: 99.83%
- **F1 Score**: 99.63%
- **Test Size**: 4,500 conversations

### Cross-Domain (`cross_domain_results/`)
Performance on 5 unseen fraud categories:
- Demonstrates strong generalization
- Detailed per-category metrics in `cross_domain_results.json`

### K-Fold Validation (`kfold_results/`)
5-fold cross-validation for robustness assessment.

## Model Artifacts

Final model stored in `roberta_final_results/`:
- `config.json` - Model configuration
- `vocab.json` - Tokenizer vocabulary
- `merges.txt` - BPE merge operations
- `tokenizer_config.json` - Tokenizer settings
- `special_tokens_map.json` - Special token mappings

## Dependencies

Install via: `pip install -r requirements_training.txt`

Main requirements:
- transformers
- torch
- datasets
- scikit-learn
