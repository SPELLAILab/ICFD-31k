"""
Dataset Quality Evaluation Package

Modular evaluation suite for fraud detection conversation dataset.
Each test is implemented in a separate module for maintainability.
"""

from .distinct_n import DistinctNTest
from .ngram_overlap import NgramOverlapTest
from .zipf_law import ZipfLawTest
from .perplexity import PerplexityTest
from .semantic_similarity import SemanticSimilarityTest
from .tsne_visualization import TSNEVisualizationTest

__all__ = [
    'DistinctNTest',
    'NgramOverlapTest',
    'ZipfLawTest',
    'PerplexityTest',
    'SemanticSimilarityTest',
    'TSNEVisualizationTest'
]

__version__ = '1.0.0'
