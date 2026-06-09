# ICFD-31k Dataset Examples

This directory contains a curated subset of ICFD-31k so the schema and chunk format can be inspected without downloading the full corpus from the [Hugging Face Hub](https://huggingface.co/datasets/rishia2220/icfd-31k).

## Contents

### Source Conversations
Full conversation JSON files organized by fraud umbrella category (20 total).

### Training Chunks
Temporal chunk-level training data corresponding to the source conversations (4476 total chunks).

## Structure

```
examples/
├── source_conversations/    # 2 conversations per umbrella
│   ├── banking/
│   ├── ecommerce/
│   ├── emergency/
│   ├── government/
│   ├── healthcare/
│   ├── jobs/
│   ├── loan/
│   ├── lottery_travel/
│   ├── tech/
│   └── utility/
└── training_chunks/         # Corresponding chunk files
    ├── banking/
    ├── ecommerce/
    ├── emergency/
    ├── government/
    ├── healthcare/
    ├── jobs/
    ├── loan/
    ├── lottery_travel/
    ├── tech/
    └── utility/
```

## Dataset Overview

- **Total Source Conversations**: 20
- **Total Training Chunks**: 4476
- **Fraud Umbrellas**: 10
- **Examples per Umbrella**: 2
- **Selection**: Random sampling (seed: 56646464)

## File Format

Each source conversation is a JSON file containing:
- Timestamped transcript
- Chunk-level annotations
- Final verdict and rationale
- Scenario metadata
- Entity extractions

Each training chunk represents a 3-second interval snapshot for streaming fraud detection.

## Full Dataset

The complete ICFD-31k dataset contains:
- 31,000 source conversations
- 1,111,071 streaming chunks
- 10 main fraud umbrellas + 5 cross-domain test categories

Refer to the main paper for complete dataset statistics and methodology.
