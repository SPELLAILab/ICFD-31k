# Dataset Quality Evaluation Suite

Modular evaluation framework for assessing the quality of the fraud detection conversation dataset.

## Structure

```
evaluation_quality/
├── __init__.py              # Package initialization
├── base_test.py             # Abstract base class for tests
├── distinct_n.py            # Linguistic Diversity (Distinct-n)
├── ngram_overlap.py         # N-gram Overlap Analysis
├── zipf_law.py              # Zipf's Law Validation
├── perplexity.py            # Perplexity Analysis (GPT-2)
├── semantic_similarity.py   # Semantic Similarity Analysis
├── tsne_visualization.py    # t-SNE 2D Visualization
└── utils.py                 # Utility functions
```

## Tests Overview

### 1. Linguistic Diversity (Distinct-n)
**File**: `distinct_n.py`  
**Purpose**: Measures vocabulary richness and detects template reuse  
**Metrics**:
- Distinct-1 (unigrams): Unique words / Total words
- Distinct-2 (bigrams): Unique bigrams / Total bigrams
- Distinct-3 (trigrams): Unique trigrams / Total trigrams

**Thresholds**:
- Distinct-1: > 0.05 (Good), > 0.10 (Excellent)
- Distinct-2: > 0.30 (Good), > 0.50 (Excellent)
- Distinct-3: > 0.50 (Good), > 0.70 (Excellent)

### 2. N-gram Overlap Analysis
**File**: `ngram_overlap.py`  
**Purpose**: Detects template/phrase reuse across conversations  
**Method**: Samples conversation pairs and measures shared n-grams  

**Thresholds**:
- Unigram overlap: < 40% (common words expected)
- Bigram overlap: < 15% (common phrases acceptable)
- Trigram overlap: < 5% (high uniqueness required)

### 3. Zipf's Law Validation
**File**: `zipf_law.py`  
**Purpose**: Validates natural language word frequency distribution  
**Method**: Plots word frequency vs rank on log-log scale  

**Thresholds**:
- MSE < 0.05: Good adherence to Zipf's Law
- -1.2 < Slope < -0.8: Natural language distribution

**Output**: `zipf_law_analysis.png`

### 4. Perplexity Analysis
**File**: `perplexity.py`  
**Purpose**: Measures text naturalness using GPT-2  
**Method**: Calculates perplexity (lower = more natural)  

**Thresholds**:
- < 50: Excellent (very natural)
- 50-80: Good (natural)
- 80-150: Acceptable
- > 150: Poor (unnatural)

**Requirements**: `transformers`, `torch`  
**Output**: `perplexity_distribution.png`

### 5. Semantic Similarity Analysis
**File**: `semantic_similarity.py`  
**Purpose**: Measures semantic separation between fraud/normal  
**Method**: Cosine similarity of sentence embeddings  

**Metrics**:
- Intra-class similarity (fraud-fraud, normal-normal): 0.4-0.6
- Inter-class similarity (fraud-normal): 0.2-0.4
- Separation score (intra - inter): > 0.10

**Requirements**: `sentence-transformers`, `scikit-learn`

### 6. t-SNE Visualization
**File**: `tsne_visualization.py`  
**Purpose**: Visual clustering analysis in 2D space  
**Method**: t-SNE dimensionality reduction of embeddings  

**Visualizations**:
- Fraud vs Normal separation
- Case type clustering (Clear Fraud, Subtle Fraud, etc.)

**Requirements**: `sentence-transformers`, `scikit-learn`  
**Output**: `tsne_visualization.png`

## Installation

```bash
# Core dependencies (required)
pip install numpy matplotlib seaborn rich

# For perplexity test
pip install torch transformers

# For semantic similarity and t-SNE
pip install sentence-transformers scikit-learn

# Or install all at once
pip install -r requirements_evaluation.txt
```

## Usage

### Run All Tests

```bash
python run_evaluation.py --source-dir output/source_conversations
```

### Sample for Faster Evaluation

```bash
# Evaluate on 1000 random conversations
python run_evaluation.py --source-dir output/source_conversations --sample-size 1000
```

### Skip Expensive Tests

```bash
# Skip perplexity and t-SNE (GPU-intensive)
python run_evaluation.py \
    --source-dir output/source_conversations \
    --skip-tests perplexity tsne
```

### Custom Output Directory

```bash
python run_evaluation.py \
    --source-dir output/source_conversations \
    --output-dir my_evaluation_results
```

## Output Files

After running evaluation, the output directory contains:

```
evaluation_results/
├── evaluation_report.md              # Comprehensive markdown report
├── all_results.json                  # Combined JSON results
├── distinct_n_results.json           # Individual test results
├── ngram_overlap_results.json
├── zipf_law_results.json
├── perplexity_results.json
├── semantic_similarity_results.json
├── tsne_results.json
├── zipf_law_analysis.png             # Zipf's Law plot
├── perplexity_distribution.png       # Perplexity histogram
└── tsne_visualization.png            # t-SNE scatter plots
```

## Adding New Tests

To add a new evaluation test:

1. Create a new file in `evaluation_quality/` (e.g., `my_test.py`)
2. Inherit from `BaseEvaluationTest`
3. Implement required methods:
   - `get_test_name()`: Return test name
   - `run()`: Execute test and return results dict

Example:

```python
from .base_test import BaseEvaluationTest

class MyTest(BaseEvaluationTest):
    def get_test_name(self) -> str:
        return "My Custom Test"
    
    def run(self) -> dict:
        # Your test logic here
        result = self.calculate_something(self.conversations)
        
        self.results = {
            'metric': result,
            'pass': result > threshold
        }
        
        self.save_results()
        return self.results
```

4. Add to `__init__.py`:
```python
from .my_test import MyTest
__all__ = [..., 'MyTest']
```

5. Add to `run_evaluation.py`:
```python
if 'my_test' not in args.skip_tests:
    test = MyTest(conversations, labels, case_types, output_dir)
    result = test.run()
    if result:
        all_results['my_test'] = result
```

## API Reference

### BaseEvaluationTest

Abstract base class for all tests.

**Constructor**:
```python
def __init__(self, conversations: List[str], labels: List[str], 
             case_types: List[str], output_dir: Path)
```

**Abstract Methods**:
- `run() -> Dict[str, Any]`: Run the test
- `get_test_name() -> str`: Return test name

**Helper Methods**:
- `save_results(filename: str = None)`: Save results to JSON
- `get_fraud_normal_split()`: Split conversations by label

### Utility Functions

**load_conversations(source_dir, sample_size)**:
- Loads conversations from JSON files
- Returns: (conversations, labels, case_types, domains)

**generate_markdown_report(results, output_dir)**:
- Generates comprehensive markdown report
- Returns: Path to report file

## Performance Tips

1. **Use sampling for initial testing**:
   ```bash
   python run_evaluation.py --sample-size 500
   ```

2. **Skip GPU-intensive tests**:
   ```bash
   python run_evaluation.py --skip-tests perplexity semantic_similarity tsne
   ```

3. **Run tests individually** (for debugging):
   ```python
   from evaluation_quality import DistinctNTest
   from evaluation_quality.utils import load_conversations
   
   convs, labels, types, _ = load_conversations('output/source_conversations')
   test = DistinctNTest(convs, labels, types, 'results')
   test.run()
   ```

4. **Parallel processing** (future enhancement):
   - Tests are currently run sequentially
   - Could be parallelized using multiprocessing

## Expected Results

For a high-quality dataset:

| Test | Expected Result |
|------|----------------|
| Distinct-1 | > 0.08 |
| Distinct-2 | > 0.40 |
| Distinct-3 | > 0.65 |
| Trigram Overlap | < 5% |
| Zipf MSE | < 0.03 |
| Perplexity | 30-60 |
| Semantic Separation | > 0.15 |

## Troubleshooting

### Missing Dependencies

```
Error: transformers library not installed
Solution: pip install transformers torch
```

### Out of Memory (GPU)

```
Solution: Reduce sample size or skip GPU tests
python run_evaluation.py --sample-size 500 --skip-tests perplexity
```

### Slow Execution

```
Solution: Use sampling and skip expensive tests
python run_evaluation.py --sample-size 1000 --skip-tests perplexity tsne
```

## References

1. Li et al. (2016) - "A Diversity-Promoting Objective Function for Neural Conversation Models"
2. Zipf, G. K. (1949) - "Human Behavior and the Principle of Least Effort"
3. van der Maaten & Hinton (2008) - "Visualizing Data using t-SNE"
4. Reimers & Gurevych (2019) - "Sentence-BERT"

## License

Released under the MIT License as part of the ICFD-31k repository.
