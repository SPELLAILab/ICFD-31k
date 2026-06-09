"""
Environment Test Script for RoBERTa Streaming Baseline
======================================================

Run this script before training to verify your environment is set up correctly.
It checks all dependencies, GPU availability, data accessibility, and disk space.

Usage:
    python test_environment.py
    
If all checks pass, you're ready to train!
"""

import sys
import os
from pathlib import Path

def print_header(text):
    """Print formatted section header"""
    print(f"\n{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}")

def print_check(name, status, details=""):
    """Print check result with status indicator"""
    indicator = "Pass" if status else "✗"
    status_text = "PASS" if status else "FAIL"
    print(f"  [{indicator}] {name}: {status_text}")
    if details:
        print(f"      {details}")

def check_python_version():
    """Check Python version (3.8-3.11 recommended)"""
    print_header("Python Version Check")
    version = sys.version_info
    version_str = f"{version.major}.{version.minor}.{version.micro}"
    
    if 3.8 <= version.minor <= 3.11 and version.major == 3:
        print_check("Python Version", True, f"Python {version_str} (Recommended)")
        return True
    elif version.minor >= 3.8:
        print_check("Python Version", True, f"Python {version_str} (May work, but not tested)")
        return True
    else:
        print_check("Python Version", False, f"Python {version_str} (Too old, need 3.8+)")
        return False

def check_dependencies():
    """Check if required packages are installed"""
    print_header("Dependency Check")
    
    dependencies = {
        'torch': 'PyTorch',
        'transformers': 'HuggingFace Transformers',
        'numpy': 'NumPy',
        'pandas': 'Pandas',
        'sklearn': 'scikit-learn',
        'tqdm': 'tqdm'
    }
    
    all_installed = True
    for package, name in dependencies.items():
        try:
            __import__(package)
            try:
                module = __import__(package)
                version = getattr(module, '__version__', 'unknown')
                print_check(name, True, f"Version {version}")
            except:
                print_check(name, True, "Installed")
        except ImportError:
            print_check(name, False, "Not installed")
            all_installed = False
    
    return all_installed

def check_gpu():
    """Check GPU availability and CUDA"""
    print_header("GPU and CUDA Check")
    
    try:
        import torch
        
        # Check CUDA availability
        cuda_available = torch.cuda.is_available()
        print_check("CUDA Available", cuda_available, 
                   "GPU training enabled" if cuda_available else "Will use CPU (slow)")
        
        if cuda_available:
            # Get GPU details
            gpu_count = torch.cuda.device_count()
            print_check("GPU Count", True, f"{gpu_count} GPU(s) detected")
            
            for i in range(gpu_count):
                gpu_name = torch.cuda.get_device_name(i)
                gpu_memory = torch.cuda.get_device_properties(i).total_memory / (1024**3)
                print_check(f"GPU {i}", True, f"{gpu_name} ({gpu_memory:.1f} GB)")
                
                if gpu_memory < 6:
                    print(f"      Warning: GPU has less than 6GB memory, may need smaller batch size")
            
            # Check CUDA version
            cuda_version = torch.version.cuda
            print_check("CUDA Version", True, f"CUDA {cuda_version}")
            
            return True
        else:
            print("  Warning: No GPU detected. Training will be very slow on CPU.")
            print("  Install CUDA and PyTorch with CUDA support for GPU training.")
            return False
            
    except ImportError:
        print_check("PyTorch", False, "PyTorch not installed")
        return False
    except Exception as e:
        print_check("GPU Check", False, f"Error: {e}")
        return False

def check_data_directory():
    """Check if training data is accessible"""
    print_header("Data Directory Check")
    
    # Default data path
    data_path = Path("../../output/training_data")
    
    if not data_path.exists():
        print_check("Data Directory", False, f"Not found at {data_path.absolute()}")
        print("  Please ensure the training_data directory is accessible.")
        return False
    
    print_check("Data Directory", True, f"Found at {data_path.absolute()}")
    
    # Count batch directories
    batch_dirs = [d for d in data_path.iterdir() if d.is_dir() and d.name.startswith('batch_')]
    print_check("Batch Folders", len(batch_dirs) > 0, f"Found {len(batch_dirs)} batch directories")
    
    # Count some chunk files (sample from first batch)
    if batch_dirs:
        first_batch = batch_dirs[0]
        chunk_files = list(first_batch.glob("*.json"))
        print_check("Chunk Files", len(chunk_files) > 0, 
                   f"Found {len(chunk_files)} chunks in {first_batch.name}")
        
        # Try to load one file
        if chunk_files:
            try:
                import json
                with open(chunk_files[0], 'r') as f:
                    data = json.load(f)
                
                # Check required fields
                required_fields = ['cumulative_transcript', 'final_verdict', 'chunk_timestamp']
                has_all_fields = all(field in data for field in required_fields)
                
                print_check("Data Format", has_all_fields, 
                           "Sample file has all required fields" if has_all_fields else "Missing fields")
                
                return has_all_fields
            except Exception as e:
                print_check("Data Loading", False, f"Error loading sample file: {e}")
                return False
    
    return True

def check_disk_space():
    """Check available disk space"""
    print_header("Disk Space Check")
    
    try:
        import shutil
        
        disk_usage = shutil.disk_usage(".")
        free_gb = disk_usage.free / (1024**3)
        total_gb = disk_usage.total / (1024**3)
        used_gb = disk_usage.used / (1024**3)
        
        print(f"  Total: {total_gb:.1f} GB")
        print(f"  Used:  {used_gb:.1f} GB")
        print(f"  Free:  {free_gb:.1f} GB")
        
        if free_gb >= 50:
            print_check("Disk Space", True, "Sufficient space (50+ GB free)")
            return True
        elif free_gb >= 30:
            print_check("Disk Space", True, "Adequate space (30-50 GB free)")
            print("  Warning: Consider freeing more space for checkpoints")
            return True
        else:
            print_check("Disk Space", False, f"Insufficient space ({free_gb:.1f} GB free)")
            print("  Need at least 30GB free for model checkpoints and logs")
            return False
            
    except Exception as e:
        print_check("Disk Space", False, f"Error checking disk space: {e}")
        return False

def check_output_directories():
    """Check if output directories exist or can be created"""
    print_header("Output Directories Check")
    
    dirs_to_check = ['models', 'results', 'logs']
    all_ok = True
    
    for dir_name in dirs_to_check:
        dir_path = Path(dir_name)
        
        if dir_path.exists():
            print_check(f"{dir_name}/", True, "Already exists")
        else:
            try:
                dir_path.mkdir(parents=True, exist_ok=True)
                print_check(f"{dir_name}/", True, "Created successfully")
            except Exception as e:
                print_check(f"{dir_name}/", False, f"Cannot create: {e}")
                all_ok = False
    
    return all_ok

def check_memory():
    """Check available RAM"""
    print_header("Memory Check")
    
    try:
        import psutil
        
        memory = psutil.virtual_memory()
        total_gb = memory.total / (1024**3)
        available_gb = memory.available / (1024**3)
        percent_used = memory.percent
        
        print(f"  Total RAM: {total_gb:.1f} GB")
        print(f"  Available: {available_gb:.1f} GB ({100-percent_used:.1f}% free)")
        
        if available_gb >= 16:
            print_check("RAM", True, "Sufficient memory (16+ GB available)")
            return True
        elif available_gb >= 8:
            print_check("RAM", True, "Adequate memory (8-16 GB available)")
            print("  Warning: Close other applications during training")
            return True
        else:
            print_check("RAM", False, f"Low memory ({available_gb:.1f} GB available)")
            print("  Need at least 8GB available RAM for training")
            return False
            
    except ImportError:
        print("  psutil not installed, skipping memory check")
        print("  Install with: pip install psutil")
        return True
    except Exception as e:
        print_check("Memory", False, f"Error checking memory: {e}")
        return True  # Don't fail on this

def run_quick_test():
    """Run a quick functionality test"""
    print_header("Quick Functionality Test")
    
    try:
        import torch
        import transformers
        
        # Test tokenizer loading
        print("  Loading RoBERTa tokenizer...", end=" ")
        tokenizer = transformers.RobertaTokenizer.from_pretrained('roberta-base')
        print("Pass")
        
        # Test model loading
        print("  Loading RoBERTa model...", end=" ")
        model = transformers.RobertaForSequenceClassification.from_pretrained(
            'roberta-base', num_labels=2
        )
        print("Pass")
        
        # Test tokenization
        print("  Testing tokenization...", end=" ")
        text = "This is a test sentence for fraud detection."
        encoding = tokenizer(text, truncation=True, padding='max_length', 
                           max_length=512, return_tensors='pt')
        print("Pass")
        
        # Test forward pass
        print("  Testing forward pass...", end=" ")
        with torch.no_grad():
            outputs = model(**encoding)
        print("Pass")
        
        print_check("Functionality Test", True, "All basic operations working")
        return True
        
    except Exception as e:
        print_check("Functionality Test", False, f"Error: {e}")
        return False

def main():
    """Run all environment checks"""
    print("\n" + "="*60)
    print("  RoBERTa Streaming Baseline - Environment Test")
    print("="*60)
    
    checks = {
        'Python Version': check_python_version(),
        'Dependencies': check_dependencies(),
        'GPU/CUDA': check_gpu(),
        'Data Directory': check_data_directory(),
        'Disk Space': check_disk_space(),
        'Output Directories': check_output_directories(),
        'Memory': check_memory(),
        'Functionality': run_quick_test()
    }
    
    # Summary
    print_header("Summary")
    
    passed = sum(1 for status in checks.values() if status)
    total = len(checks)
    
    print(f"\n  Passed: {passed}/{total} checks")
    
    if all(checks.values()):
        print("\n  Pass All checks passed! Environment is ready for training.")
        print("\n  Next steps:")
        print("    1. Review TRAINING_GUIDE.md for detailed instructions")
        print("    2. Run a quick test: python train_roberta_streaming.py --max_samples 10000")
        print("    3. Start full training: python train_roberta_streaming.py")
        return 0
    else:
        print("\n  ✗ Some checks failed. Please fix the issues above before training.")
        print("\n  Failed checks:")
        for check_name, status in checks.items():
            if not status:
                print(f"    - {check_name}")
        
        print("\n  See TRAINING_GUIDE.md for troubleshooting help.")
        return 1

if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)
