# RoBERTa-2b: Streaming Detection

Fine-tuned RoBERTa-base for chunk-level fraud detection in streaming scenarios.

## Approach

- **Architecture**: RoBERTa-base (125M parameters)
- **Input**: Cumulative transcript at 3-second intervals
- **Task**: Binary classification at each temporal chunk
- **Training**: 619,008 temporal chunks from 24,800 conversations

## Key Innovation

Enables real-time fraud detection:
- Classify conversation as it unfolds
- Early detection (median 30 s, as early as 6 s into the call)
- Streaming-compatible architecture

## Files

### Training
- `train_roberta_streaming.py` - Main training script with temporal chunking
- `requirements_training.txt` - Training dependencies

### Testing
- `test_cross_domain.py` - Generalization to unseen fraud types
- `test_environment.py` - Setup validation

## Results

### Main Test Set (`final_model/results/`)
- **Accuracy**: 95.41%
- **Precision**: 95.50%
- **Recall**: 95.67%
- **F1 Score**: 95.59%
- **Test Size**: 129,116 chunks

### Cross-Domain (`cross_domain_results/`)
Performance on chunk-level classification for unseen categories.

### Training Metrics
Stored in `final_model/results/training_metrics.json`:
- Epoch-wise loss curves
- Validation metrics
- Data split statistics

## Model Artifacts

Final model in `final_model/`:
- Configuration and tokenizer files
- Training logs in `logs/` (TensorBoard events)
- Predictions and metrics in `results/`

## Use Case

This model enables:
1. **Real-time fraud detection** during live conversations
2. **Early warning systems** for fraud prevention
3. **Progressive analysis** of conversation evolution

## Dependencies

Install via: `pip install -r requirements_training.txt`

Main requirements:
- transformers
- torch
- datasets
- tensorboard
