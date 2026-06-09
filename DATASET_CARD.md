# Dataset Card for ICFD-31k

> Companion dataset for the IJCAI-ECAI 2026 paper *ICFD-31k: A Large-Scale Dataset and Benchmark for Real-Time Conversational Fraud Detection* (AI for Social Good track).

## Dataset Summary

ICFD-31k is a synthetic Indian conversational fraud dataset for static and streaming fraud detection. It contains phone-call style conversations in English/Hinglish, covering 10 primary fraud umbrellas and 5 cross-domain unseen fraud types.

## Access

```python
from datasets import load_dataset

dataset = load_dataset("rishia2220/icfd-31k")
```

## Tasks

- Static classification: classify a full transcript as fraud or normal.
- Streaming classification: classify cumulative 3-second chunks during an ongoing conversation.
- Cross-domain generalization: evaluate on unseen fraud categories.

## Data Fields

Each source conversation contains:

- `transcript`: speaker turns with text and timestamps.
- `key_entities`: extracted organizations, products, and sensitive data requests.
- `multimodal_analysis`: simulated paralinguistic cues (dominant/secondary emotion, pace, confidence).
- `chunk_level_analysis`: timestamped streaming labels and rationales.
- `final_slow_thinking_rationale`: final explanation.
- `final_verdict`: fraud/normal verdict.
- `violated_policies`: applicable policy violations.
- `scenario`, `agent_persona`, `customer_persona`: generation context.

Each streaming chunk contains:

- `session_id`
- `chunk_timestamp`
- `cumulative_transcript`
- `verdict_at_chunk`
- `rationale_at_chunk`
- source scenario metadata

## Dataset Statistics

- Source conversations: 31,000
- Streaming chunks: 1,111,071
- Main fraud umbrellas: 10
- Cross-domain fraud types: 5
- Average conversation length: 115.8 seconds

### Splits

| Split | Source conversations | Streaming chunks |
|---|---|---|
| Train | 21,000 | 712,316 |
| Validation | 4,500 | 173,813 |
| Test | 4,500 | 179,827 |
| Cross-domain | 1,000 | 45,115 |
| **Total** | **31,000** | **1,111,071** |

Streaming chunks inherit the split of their source conversation, so chunks from one call never appear in more than one split.

## Human Validation

Expert validation used cybersecurity, computational linguistics, and fraud-detection perspectives. The sampled validation subset yielded mean pairwise Cohen's Kappa of 0.534, indicating moderate inter-annotator agreement.

## Limitations

- The conversations are synthetic and do not replace validation on real calls.
- Real deployment must account for ASR errors, accents, dialect variation, background noise, and changing scam tactics.
- The dataset uses a defensive-use license because fraud conversations have dual-use risk.

## Intended Use

Permitted uses include academic research, fraud prevention, defensive model development, and educational work in conversational safety.

Prohibited uses include scam-script generation, offensive social-engineering training, fraud automation, or any use that facilitates harm.

