#!/usr/bin/env python3
import sys
import numpy as np
import matplotlib.pyplot as plt

def analyze_pcs(eigenval_file):
    # Read eigenvalues
    eigenvals = np.loadtxt(eigenval_file)
    
    # Calculate proportion of variance explained
    total_var = np.sum(eigenvals)
    prop_var = eigenvals / total_var
    cum_var = np.cumsum(prop_var)
    
    # Create scree plot
    plt.figure(figsize=(10, 6))
    
    # Plot individual proportion of variance
    plt.subplot(1, 2, 1)
    plt.plot(range(1, len(prop_var) + 1), prop_var, 'bo-')
    plt.xlabel('Principal Component')
    plt.ylabel('Proportion of Variance Explained')
    plt.title('Scree Plot')
    
    # Plot cumulative proportion
    plt.subplot(1, 2, 2)
    plt.plot(range(1, len(cum_var) + 1), cum_var, 'ro-')
    plt.xlabel('Principal Component')
    plt.ylabel('Cumulative Proportion of Variance')
    plt.title('Cumulative Variance Plot')
    plt.axhline(y=0.8, color='gray', linestyle='--', label='80% threshold')
    
    plt.tight_layout()
    plt.savefig('pc_analysis.png')
    
    # Print summary
    print("\nPrincipal Component Analysis Summary:")
    print("=====================================")
    print(f"{'PC':<4} {'Prop. Var':<10} {'Cum. Var':<10}")
    print("-" * 24)
    for i, (prop, cum) in enumerate(zip(prop_var, cum_var), 1):
        print(f"{i:<4} {prop:>.4f}     {cum:>.4f}")
        if cum > 0.8 and i > 1:  # Skip first PC to avoid tiny variations
            recommended_pcs = i
            break
    else:
        recommended_pcs = len(prop_var)
    
    print(f"\nRecommended number of PCs: {recommended_pcs}")
    print(f"(Explains {cum_var[recommended_pcs-1]*100:.1f}% of total variance)")
    
    return recommended_pcs

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python pc_analyzer.py eigenval_file")
        sys.exit(1)
    
    n_pcs = analyze_pcs(sys.argv[1])
