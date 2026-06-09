#!/usr/bin/env python3
"""
Cross-Domain Test Data Generation Script

Generates 1,000 conversations across 5 NEW fraud domains for testing model generalization.

Domains:
1. Cryptocurrency/NFT (200 conversations)
2. Romance/Dating (200 conversations)
3. Charity/Donation (200 conversations)
4. Investment/Real Estate (200 conversations)
5. Tax/IRS/SSN (200 conversations)

Usage:
    python generate_cross_domain_test.py
    
Or generate one domain at a time:
    python generate_cross_domain_test.py --domain crypto
"""

import subprocess
import sys
import time
from pathlib import Path

# Domain configurations
DOMAINS = {
    'crypto': {
        'name': 'Cryptocurrency/NFT Scams',
        'scenarios': 'data/testing/scenarios_crypto.txt',
        'personas': 'data/testing/personas_cross_domain.txt'
    },
    'romance': {
        'name': 'Romance/Dating Scams',
        'scenarios': 'data/testing/scenarios_romance.txt',
        'personas': 'data/testing/personas_cross_domain.txt'
    },
    'charity': {
        'name': 'Charity/Donation Scams',
        'scenarios': 'data/testing/scenarios_charity.txt',
        'personas': 'data/testing/personas_cross_domain.txt'
    },
    'investment': {
        'name': 'Investment/Real Estate Scams',
        'scenarios': 'data/testing/scenarios_investment.txt',
        'personas': 'data/testing/personas_cross_domain.txt'
    },
    'tax': {
        'name': 'Tax/IRS/SSN Scams',
        'scenarios': 'data/testing/scenarios_tax_irs.txt',
        'personas': 'data/testing/personas_cross_domain.txt'
    }
}

def check_files_exist():
    """Verify all required files exist"""
    print("Checking required files...")
    
    missing_files = []
    
    for domain_key, domain_info in DOMAINS.items():
        scenarios = Path(domain_info['scenarios'])
        personas = Path(domain_info['personas'])
        
        if not scenarios.exists():
            missing_files.append(str(scenarios))
        if not personas.exists():
            missing_files.append(str(personas))
    
    if missing_files:
        print("\nFAIL: ERROR: Missing required files:")
        for f in missing_files:
            print(f"  - {f}")
        print("\nPlease ensure all scenario and persona files are created.")
        return False
    
    print("✓ All required files found\n")
    return True


def generate_domain(domain_key):
    """Generate data for a specific domain"""
    domain_info = DOMAINS[domain_key]
    
    print("="*70)
    print(f"Generating: {domain_info['name']}")
    print("="*70)
    print(f"Scenarios: {domain_info['scenarios']}")
    print(f"Personas:  {domain_info['personas']}")
    print(f"Expected:  ~200 conversations")
    print("="*70)
    print()
    
    # Run generation
    cmd = [
        'python', 'generate_dataset.py',
        '--scenarios', domain_info['scenarios'],
        '--personas', domain_info['personas'],
        '--multiplier', '1'
    ]
    
    print(f"Running: {' '.join(cmd)}\n")
    
    start_time = time.time()
    result = subprocess.run(cmd, capture_output=False, text=True)
    elapsed = time.time() - start_time
    
    if result.returncode == 0:
        print(f"\n✓ {domain_info['name']} completed in {elapsed/60:.1f} minutes")
        return True
    else:
        print(f"\nFAIL: {domain_info['name']} failed with error code {result.returncode}")
        return False


def generate_all_domains():
    """Generate data for all domains"""
    print("\n" + "="*70)
    print("Cross-Domain Test Data Generation")
    print("="*70)
    print("This will generate 1,000 conversations across 5 new fraud domains")
    print("Total estimated time: 2-3 hours")
    print("="*70)
    print()
    
    if not check_files_exist():
        return False
    
    input("Press Enter to start generation (or Ctrl+C to cancel)...")
    print()
    
    total_start = time.time()
    results = {}
    
    for i, (domain_key, domain_info) in enumerate(DOMAINS.items(), 1):
        print(f"\n[{i}/5] Starting {domain_info['name']}...")
        results[domain_key] = generate_domain(domain_key)
        print()
        
        if results[domain_key]:
            print(f"✓ Domain {i}/5 complete")
        else:
            print(f"FAIL: Domain {i}/5 failed")
            user_input = input("Continue with remaining domains? (y/n): ")
            if user_input.lower() != 'y':
                break
    
    total_elapsed = time.time() - total_start
    
    # Summary
    print("\n" + "="*70)
    print("Generation Summary")
    print("="*70)
    
    successful = sum(1 for v in results.values() if v)
    failed = len(results) - successful
    
    print(f"Total time: {total_elapsed/3600:.1f} hours ({total_elapsed/60:.1f} minutes)")
    print(f"Successful domains: {successful}/5")
    print(f"Failed domains: {failed}/5")
    print()
    
    for domain_key, success in results.items():
        status = "✓" if success else "❌"
        print(f"  {status} {DOMAINS[domain_key]['name']}")
    
    print("\n" + "="*70)
    
    if successful == 5:
        print("\n🎉 All domains generated successfully!")
        print("\nNext steps:")
        print("1. Check output/source_conversations/ for generated batches")
        print("2. Run cross-domain test:")
        print("   cd baseline/roberta-2a")
        print("   python test_cross_domain.py --test_data ../../output/source_conversations")
        print()
        return True
    else:
        print(f"\nWARN: {failed} domain(s) failed. Review errors above.")
        return False


def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Generate cross-domain test data for fraud detection",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        '--domain',
        choices=['crypto', 'romance', 'charity', 'investment', 'tax', 'all'],
        default='all',
        help='Generate specific domain or all domains (default: all)'
    )
    
    parser.add_argument(
        '--check-only',
        action='store_true',
        help='Only check if required files exist, dont generate'
    )
    
    args = parser.parse_args()
    
    if args.check_only:
        return 0 if check_files_exist() else 1
    
    if args.domain == 'all':
        success = generate_all_domains()
    else:
        if not check_files_exist():
            return 1
        success = generate_domain(args.domain)
    
    return 0 if success else 1


if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\nGeneration cancelled by user")
        sys.exit(1)
