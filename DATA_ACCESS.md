# Data Access

The full ICFD-31k corpus is hosted on the Hugging Face Hub. This repository holds the code, metadata, documentation, and a small set of representative examples; the complete dataset is not stored in Git because it is too large to clone comfortably.

## Download

**https://huggingface.co/datasets/rishia2220/icfd-31k**

```python
from datasets import load_dataset

dataset = load_dataset("rishia2220/icfd-31k")
```

## What Is in the Repository

- `examples/` — representative source conversations and streaming chunks for inspecting the schema without downloading the full corpus.
- `dataset_manifest.example.jsonl` — the manifest format used to track released shards.
- `scripts/download_data.py` and `scripts/verify_checksums.py` — utilities for mirroring a manifest locally and verifying shard integrity.

## Format

Source conversations are released as Zstandard-compressed JSONL (`*.jsonl.zst`); the nested transcript structure stays human-inspectable. Streaming chunks are released as Parquet for compact, columnar access during training.

```text
source_conversations/
  train-*.jsonl.zst
  validation-*.jsonl.zst
  test-*.jsonl.zst
  cross_domain-*.jsonl.zst

streaming_chunks/
  train-*.parquet
  validation-*.parquet
  test-*.parquet
  cross_domain-*.parquet
```

## Integrity

Each release is described by a `dataset_manifest.jsonl` with one row per shard, recording its path, download URL, size, and SHA-256 checksum:

```json
{"split":"train","task":"static","path":"source_conversations/train-00000-of-00010.jsonl.zst","url":"https://...","bytes":123456789,"sha256":"..."}
```

After downloading, verify the shards against the manifest:

```bash
python scripts/verify_checksums.py --manifest dataset_manifest.jsonl --root ./data_full
```
