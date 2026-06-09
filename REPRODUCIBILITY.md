# Reproducibility Guide

This repository supports three levels of reproducibility.

## 1. Inspect Examples

Representative examples are included under:

```text
examples/source_conversations/
examples/training_chunks/
```

These files show the source JSON schema and chunk-level training format without requiring the full dataset download.

## 2. Re-run Generation

Install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Set the API key:

```bash
export GROQ_API_KEY="your_key_here"
```

Run:

```bash
python generate_dataset.py --dry-run
python generate_dataset.py
```

The generation pipeline combines scenarios, personas, and entity libraries from `data/`, then expands each source conversation into streaming chunks.

## 3. Re-run Diagnostics

Install evaluation dependencies:

```bash
pip install -r requirements_evaluation.txt
```

Run:

```bash
python run_evaluation.py
```

The diagnostic modules are in `evaluation/evaluation_quality/`.

## Baseline Reproduction

Baseline scripts are under:

```text
baselines/gemma-0shot-a/
baselines/roberta-2a/
baselines/roberta-2b/
```

Use the README in each subfolder for model-specific commands. The RoBERTa baselines assume the full source-conversation and streaming-chunk files are available locally through the dataset manifest workflow in `DATA_ACCESS.md`.

## Determinism Notes

Generation uses LLM sampling and therefore cannot be perfectly deterministic unless the provider, model version, prompt, temperature, and sampled outputs are frozen. For exact dataset reproduction, use the released dataset shards and verify their checksums. For method reproduction, regenerate from the same persona/scenario/entity libraries and report the generation date/model.
