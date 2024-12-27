#!/usr/bin/env python3

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def calculate_variance(file_path):
    """Calculate variance explained by top 1% SNPs"""
    try:
        # Read MLMA file
        df = pd.read_csv(file_path, sep='\t')
        
        # Calculate genetic variance per SNP
        df['vg'] = 2 * df['Freq'] * (1 - df['Freq']) * (df['b'] ** 2)
        
        # Total genetic variance
        total_vg = df['vg'].sum()
        
        # Get top 1% SNPs
        num_top = int(np.ceil(len(df) * 0.01))
        top_snps = df.nsmallest(num_top, 'p')
        top_vg = top_snps['vg'].sum()
        
        # Calculate percentage
        percent_explained = (top_vg/total_vg) * 100
        
        return {
            'total_vg': total_vg,
            'top_vg': top_vg,
            'percent': percent_explained,
            'n_snps': len(df),
            'n_top': num_top
        }
    except Exception as e:
        print(f"Error processing {file_path}: {str(e)}")
        return None

def plot_variance_results(results):
    """Create horizontal bar plot of variance explained"""
    # Create DataFrame for plotting
    df_plot = pd.DataFrame({
        'Trait': list(results.keys()),
        'Top 1% Vg (%)': [results[trait]['percent'] for trait in results],
        'Remaining Vg (%)': [100 - results[trait]['percent'] for trait in results]
    })

    # Sort by variance explained
    df_plot = df_plot.sort_values('Top 1% Vg (%)', ascending=True)

    # Create figure and axes with extra width for legend
    fig, ax = plt.subplots(figsize=(12, max(6, len(results) * 0.5)))
    
    # Plot bars
    y_pos = np.arange(len(df_plot))
    
    # Plot remaining variance (bottom bar)
    remaining = ax.barh(y_pos, df_plot['Remaining Vg (%)'], 
                       color='#e74c3c', label='Remaining SNPs')
    
    # Plot top 1% variance (top bar)
    top = ax.barh(y_pos, df_plot['Top 1% Vg (%)'],
                  color='#2ecc71', label='Top 1% SNPs')
    
    # Add percentage labels inside the bars
    for i, row in df_plot.iterrows():
        # Label for top 1% SNPs
        width_top = row['Top 1% Vg (%)']
        ax.text(width_top/2, i, f'{width_top:.1f}%',
                va='center', ha='center', color='white')
        
        # Label for remaining SNPs
        width_remaining = row['Remaining Vg (%)']
        ax.text(width_top + width_remaining/2, i, f'{width_remaining:.1f}%',
                va='center', ha='center', color='white')
    
    # Customize plot
    ax.set_yticks(y_pos)
    ax.set_yticklabels(df_plot['Trait'])
    ax.set_xlabel('Percentage of Total Genetic Variance Explained')
    ax.set_title('Proportion of Genetic Variance Explained by Top 1% SNPs vs Remaining SNPs')
    
    # Move legend outside to the right
    ax.legend(bbox_to_anchor=(1.15, 0.5), loc='center left')
    
    # Adjust layout to prevent label cutoff
    plt.tight_layout()
    
    # Save plot with extra space for legend
    plt.savefig('variance_explained.png', dpi=300, bbox_inches='tight')
    plt.close()

def save_results_to_csv(results):
    """Save numerical results to CSV file"""
    df_results = pd.DataFrame({
        'Trait': list(results.keys()),
        'Total_SNPs': [results[trait]['n_snps'] for trait in results],
        'Top_1%_SNPs': [results[trait]['n_top'] for trait in results],
        'Total_Vg': [results[trait]['total_vg'] for trait in results],
        'Top_1%_Vg': [results[trait]['top_vg'] for trait in results],
        'Percent_Variance_Explained': [results[trait]['percent'] for trait in results]
    })
    df_results.to_csv('variance_results.csv', index=False)

def main():
    # Get all .mlma files in current directory
    mlma_files = [f for f in os.listdir() if f.endswith('.mlma')]
    
    if not mlma_files:
        print("No .mlma files found in current directory!")
        return
        
    print(f"Found {len(mlma_files)} .mlma files")
    results = {}

    # Process each file
    for file in mlma_files:
        trait = input(f"Enter trait name for {file}: ")
        result = calculate_variance(file)
        
        if result:
            results[trait] = result
            print(f"\nResults for {trait}:")
            print(f"Total SNPs: {result['n_snps']}")
            print(f"Top {result['n_top']} SNPs explain {result['percent']:.2f}% of total variance")
            print(f"Total genetic variance: {result['total_vg']:.2f}")
            print("-" * 50)

    if results:
        # Create visualization
        plot_variance_results(results)
        print("\nPlot saved as 'variance_explained.png'")
        
        # Save numerical results
        save_results_to_csv(results)
        print("Numerical results saved as 'variance_results.csv'")
    else:
        print("No valid results to plot!")

if __name__ == "__main__":
    main()
