# Gemma 2 Zero-Shot Baseline

Zero-shot fraud detection using Google's Gemma 2 (2B parameters).

## Approach

Direct prompting without any fine-tuning:
- Model reads full conversation transcript
- Prompted to classify as fraud or legitimate
- No training on ICFD-31k dataset

## Files

- `test_gemma_0shot.py` - Main evaluation script
- `analyze_results.py` - Metrics calculation and analysis
- `worker_manager.py` - Parallel processing for efficiency
- `tui_display.py` - Terminal UI for progress tracking
- `test_setup.py` - Environment validation
- `requirements.txt` - Python dependencies

## Results

Located in `results/`:
- `results.txt` - Human-readable summary
- `metrics.json` - Structured performance metrics
- `summary.json` - Aggregate statistics
- `detailed_results.csv` - Per-conversation predictions

### Performance
- **Accuracy**: 28.94%
- **Precision**: 93.58%
- **Recall**: 22.16%
- **F1 Score**: 35.83%
- **Test Set**: 5,000 conversations

## Key Insights

Zero-shot performance illustrates:
1. High precision but low recall: the model is conservative and misses most fraud without task-specific training.
2. The substantial gap to the fine-tuned RoBERTa baselines motivates training on ICFD-31k.

## Dependencies

Install via: `pip install -r requirements.txt`

Main requirements:
- transformers
- torch
- pandas
- numpy
