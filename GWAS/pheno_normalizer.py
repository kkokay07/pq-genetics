#!/usr/bin/env python3
import argparse
from math import sqrt, pi, exp, log
from statistics import mean, stdev

def read_phenotype_file(filename):
    """Read phenotype file"""
    fid, iid, pheno = [], [], []
    with open(filename, 'r') as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) >= 3 and parts[2] != '-9':  # Skip missing values
                try:
                    pheno_val = float(parts[2])
                    fid.append(parts[0])
                    iid.append(parts[1])
                    pheno.append(pheno_val)
                except ValueError:
                    continue  # Skip header or non-numeric values
    return fid, iid, pheno

def get_ranks(values):
    """Get ranks of values"""
    n = len(values)
    indexed_values = list(enumerate(values))
    indexed_values.sort(key=lambda x: x[1])
    
    # Calculate ranks
    ranks = [0] * n
    for rank, (index, _) in enumerate(indexed_values, 1):
        ranks[index] = rank
    
    return ranks

def inverse_normal_cdf_approx(p):
    """Approximate inverse normal CDF (probit function)"""
    if p <= 0 or p >= 1:
        return 0
    
    # Constants for the approximation
    c = [2.515517, 0.802853, 0.010328]
    d = [1.432788, 0.189269, 0.001308]
    
    if p <= 0.5:
        t = sqrt(-2.0 * log(p))
    else:
        t = sqrt(-2.0 * log(1.0 - p))
    
    num = (c[2]*t + c[1])*t + c[0]
    den = ((d[2]*t + d[1])*t + d[0])*t + 1.0
    
    if p <= 0.5:
        return -(t - num/den)
    return t - num/den

def quantile_normalize(values):
    """Perform quantile normalization"""
    n = len(values)
    ranks = get_ranks(values)
    
    # Convert ranks to probabilities and then to normal quantiles
    normalized = []
    for rank in ranks:
        p = (rank - 0.5) / n
        normalized.append(inverse_normal_cdf_approx(p))
    
    return normalized

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Normalize phenotype data to standard normal distribution')
    parser.add_argument('input', help='Input phenotype file (FID IID Phenotype format)')
    parser.add_argument('--out', help='Output file name', default='normalized.txt')
    args = parser.parse_args()
    
    try:
        # Read data
        fid, iid, pheno = read_phenotype_file(args.input)
        print(f"Read {len(pheno)} phenotype records")
        
        # Original statistics
        print("\nOriginal Statistics:")
        print(f"Mean: {mean(pheno):.3f}")
        print(f"Standard Deviation: {stdev(pheno):.3f}")
        
        # Normalize
        print("\nPerforming normalization...")
        normalized = quantile_normalize(pheno)
        
        # Normalized statistics
        print("\nNormalized Statistics:")
        print(f"Mean: {mean(normalized):.3f}")
        print(f"Standard Deviation: {stdev(normalized):.3f}")
        
        # Save normalized phenotypes
        print(f"\nSaving normalized phenotypes to {args.out}...")
        with open(args.out, 'w') as f:
            for i in range(len(fid)):
                f.write(f"{fid[i]}\t{iid[i]}\t{normalized[i]:.6f}\n")
        
        print(f"Done! Normalized phenotypes saved to '{args.out}'")
        
    except FileNotFoundError:
        print(f"Error: {args.input} file not found!")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
