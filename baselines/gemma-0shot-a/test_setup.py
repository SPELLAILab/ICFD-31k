"""
Quick Test for Gemma Zero-Shot Setup
===================================

Tests the setup with a small number of samples to ensure everything works.
"""

import subprocess
import sys
from pathlib import Path


def test_dependencies():
    """Test if all required dependencies are available."""
    print("Testing dependencies...")
    
    try:
        import torch
        print(f"   PyTorch: {torch.__version}__}")
        
        if torch.cuda.is_available():
            print(f"   CUDA: {torch.cuda.device_count()} GPUs available")
            for i in range(torch.cuda.device_count()):
                name = torch.cuda.get_device_name(i)
                mem_gb = torch.cuda.get_device_properties(i).total_memory / (1024**3)
                print(f"      GPU {i}: {name} ({mem_gb:.1f}GB)")
        else:
            print("   CUDA not available - GPU required for Gemma")
            return False
            
    except ImportError:
        print("   PyTorch not found")
        return False
    
    try:
        import transformers
        print(f"   Transformers: {transformers.__version__}")
    except ImportError:
        print("   Transformers not found")
        return False
    
    try:
        from rich.console import Console
        print(f"   Rich (for TUI)")
    except ImportError:
        print("   Rich not found - install with: pip install rich")
        return False
    
    return True


def test_data_availability():
    """Test if training data is available."""
    print("\nTesting data availability...")
    
    data_dir = Path("../../output/training_data")
    if not data_dir.exists():
        print(f"   Training data directory not found: {data_dir}")
        print("      Please run data generation first")
        return False
    
    batch_dirs = list(data_dir.glob("batch_*"))
    if not batch_dirs:
        print(f"   No batch directories found in: {data_dir}")
        return False
    
    print(f"   Found {len(batch_dirs)} batch directories")
    
    # Count total conversations
    total_convs = 0
    for batch_dir in batch_dirs[:3]:  # Check first 3 batches
        conv_files = list(batch_dir.glob("*.json"))
        total_convs += len(conv_files)
    
    print(f"   Sample count: ~{total_convs * len(batch_dirs) // 3:,} conversations")
    
    return True


def run_quick_test():
    """Run a quick test with limited samples."""
    print("\nRunning quick test (10 samples)...")
    
    cmd = [
        sys.executable, "test_gemma_0shot.py",
        "--max_samples", "10",
        "--num_workers", "1",
        "--output_dir", "./test_results"
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            print("   Quick test passed")
            print("   Sample output:")
            # Show last few lines of output
            lines = result.stdout.strip().split('\n')
            for line in lines[-10:]:
                if line.strip():
                    print(f"      {line}")
            return True
        else:
            print(f"   Quick test failed (exit code: {result.returncode})")
            print(f"   Error: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("   Quick test timed out (>5 minutes)")
        return False
    except Exception as e:
        print(f"   Quick test error: {e}")
        return False


def main():
    print("Testing Gemma Zero-Shot Setup")
    print("=" * 50)
    
    # Test dependencies
    if not test_dependencies():
        print("\nDependency test failed. Please install required packages:")
        print("   pip install -r requirements.txt")
        return 1
    
    # Test data
    if not test_data_availability():
        print("\nData test failed. Please ensure training data is available.")
        return 1
    
    print("\nAll tests passed. Ready for full evaluation.")
    print("\nNext steps:")
    print("   1. Run full evaluation:")
    print("      python test_gemma_0shot.py --max_samples 1000 --num_workers 4")
    print("   2. Analyze results:")
    print("      python analyze_results.py --results_dir ./results")
    
    return 0


if __name__ == '__main__':
    exit(main())