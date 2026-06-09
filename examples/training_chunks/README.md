# Training Chunks

This directory contains temporal chunk-level training data for the conversations in `source_conversations/`.

## Format

Each chunk represents a 3-second interval snapshot with:

- `cumulative_transcript`: All conversation text up to this timestamp
- `label`: Binary fraud label (YES/NO) at this point
- `timestamp`: Current time in seconds
- `session_id`: Links to source conversation
- `rationale_at_chunk`: Reasoning at this temporal point

## Purpose

These chunks enable:

1. **Streaming Detection**: Train models to detect fraud in real-time
2. **Early Detection**: Evaluate how quickly fraud can be identified
3. **Temporal Analysis**: Study how fraud signals evolve over time

## Organization

Chunks are organized by the same umbrella categories as source conversations.
Each source conversation typically generates 20-40 chunks (depending on length).

## Chunking Strategy

- **Fraud cases**: Fully chunked at 3-second intervals
- **Normal cases**: Sparsely sampled (1-2 random chunks)
- **Total chunks**: 4476 across 20 conversations
