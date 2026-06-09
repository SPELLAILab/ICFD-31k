# ICFD-31k Baseline Models

This directory contains three baseline models for fraud detection on ICFD-31k.

## Models

### 1. Gemma 0-Shot (`gemma-0shot-a/`)
Zero-shot prompting with Google's Gemma 2 (2B parameters).

- **Approach**: Direct prompting without fine-tuning
- **Test Set**: 5,000 conversations
- **Accuracy**: 28.94%
- **Precision**: 93.58% | **Recall**: 22.16%
- **F1 Score**: 35.83%

### 2. RoBERTa-2a (`roberta-2a/`)
Fine-tuned RoBERTa-base on full conversation transcripts.

- **Approach**: Full-context classification
- **Training**: 24,800 conversations
- **Test Set**: 4,500 conversations
- **Accuracy**: 99.62%
- **Precision**: 99.44% | **Recall**: 99.83%
- **F1 Score**: 99.63%

### 3. RoBERTa-2b (`roberta-2b/`)
Fine-tuned RoBERTa-base on temporal chunks for streaming detection.

- **Approach**: Chunk-level classification (3-second intervals)
- **Training**: 619,008 chunks
- **Test Set**: 129,116 chunks
- **Accuracy**: 95.41%
- **Precision**: 95.50% | **Recall**: 95.67%
- **F1 Score**: 95.59%

## Contents

Each model directory includes:
- Training scripts
- Testing/evaluation scripts
- Requirements files
- Results (metrics, predictions, logs)

## Cross-Domain Testing

Both RoBERTa models include cross-domain evaluation on 5 unseen fraud categories:
- Charity scams
- Cryptocurrency fraud
- Investment scams
- Romance fraud
- Tax/IRS impersonation

Results demonstrate model generalization to novel fraud types.

## Usage

Refer to individual model directories for setup and execution instructions.
All models use the same train/test splits for fair comparison.
