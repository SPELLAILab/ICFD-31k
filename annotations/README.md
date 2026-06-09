# Human Annotation Results

This directory contains human annotation data for ICFD-31k dataset validation.

## Contents

### Individual Annotations
- `annotation_1.csv` - Annotator 1 labels (25 conversations)
- `annotation_2.csv` - Annotator 2 labels (25 conversations)
- `annotation_3.csv` - Annotator 3 labels (25 conversations)
- `annotation_4.csv` - Annotator 4 labels (25 conversations)
- `annotation_5.csv` - Annotator 5 labels (25 conversations)

### Consensus Data
- `consensus_labels.csv` - Final consensus labels with agreement statistics
- `overlap_analysis.csv` - Inter-annotator agreement analysis

## Annotation Protocol

Each annotator independently labeled 25 conversations sampled from ICFD-31k:
- Multi-class classification (Definite Fraud/Definite Legitimate/Probable Fraud/Probable Legitimate/Unclear)
- 15 overlap conversations for inter-annotator agreement
- Blind annotation (no access to other annotators' labels)

## Results

- **Sample Size**: 25 conversations per annotator (15 overlap, 10 unique)
- **Annotators**: 5 domain experts
- **Inter-Annotator Agreement (mean pairwise Cohen's Kappa)**: 0.534

## File Format

CSV files contain:
- `conversation_id`: Unique conversation identifier
- `fraud_label`: Binary label (1=Fraud, 0=Legitimate)
- `rationale`: Optional explanation for label
- `annotator_id`: Annotator identifier (in individual files)
- `agreement_count`: Number of annotators in consensus (in consensus file)
