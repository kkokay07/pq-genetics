#!/usr/bin/env python3

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import os
import sys

def process_inbreeding_data(file_path):
    """Read and process inbreeding coefficient data."""
    try:
        # Read the data
        df = pd.read_csv(file_path, sep='\t')
        
        # Set negative F values to 0
        df[['Fhat1', 'Fhat2', 'Fhat3']] = df[['Fhat1', 'Fhat2', 'Fhat3']].clip(lower=0)
        
        # Calculate population means
        pop_means = df.groupby('FID')[['Fhat1', 'Fhat2', 'Fhat3']].mean()
        
        return pop_means
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)

def plot_inbreeding_coefficients(pop_means, output_file):
    """Create bar plots for inbreeding coefficients."""
    # Set up the figure with three subplots
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 10))
    fig.suptitle('Inbreeding Coefficients', fontsize=16, y=0.95)
    
    # Color palette
    colors = ['#FF9999', '#66B2FF', '#99FF99']
    
    # Plot settings
    bar_width = 0.6
    alpha = 0.7
    
    # Funi (Fhat1) plot
    ax1.bar(range(len(pop_means)), pop_means['Fhat1'], 
            color=colors[0], alpha=alpha, width=bar_width)
    ax1.set_ylabel('F_UNI')
    ax1.set_ylim(0, max(pop_means['Fhat1']) * 1.2)
    
    # FGRM (Fhat2) plot
    ax2.bar(range(len(pop_means)), pop_means['Fhat2'], 
            color=colors[1], alpha=alpha, width=bar_width)
    ax2.set_ylabel('F_GRM')
    ax2.set_ylim(0, max(pop_means['Fhat2']) * 1.2)
    
    # Fhom (Fhat3) plot
    ax3.bar(range(len(pop_means)), pop_means['Fhat3'], 
            color=colors[2], alpha=alpha, width=bar_width)
    ax3.set_ylabel('F_HOM')
    ax3.set_ylim(0, max(pop_means['Fhat3']) * 1.2)
    
    # Customize all subplots
    for ax in [ax1, ax2, ax3]:
        # Add value labels on top of bars
        for i, v in enumerate(ax.containers[0]):
            ax.text(v.get_x() + v.get_width()/2, v.get_height(),
                   f'{v.get_height():.2f}',
                   ha='center', va='bottom')
        
        # Set x-ticks and labels
        ax.set_xticks(range(len(pop_means)))
        ax.set_xticklabels(pop_means.index, rotation=45, ha='right')
        
        # Add grid
        ax.grid(True, axis='y', linestyle='--', alpha=0.3)
        
        # Remove top and right spines
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
    
    # Adjust layout
    plt.tight_layout()
    
    try:
        # Save the plot with 600 DPI
        plt.savefig(output_file, dpi=600, bbox_inches='tight')
        print(f"Plot saved successfully as {output_file}")
    except Exception as e:
        print(f"Error saving plot: {e}")
    finally:
        plt.close()

def main():
    # Get input file name from user
    input_file = input("Please enter the input .ibc file name: ").strip()
    
    # Check if file exists
    if not os.path.exists(input_file):
        print(f"Error: File '{input_file}' not found.")
        sys.exit(1)
    
    # Generate output file name by replacing .ibc with .png
    if input_file.lower().endswith('.ibc'):
        output_file = input_file[:-4] + '.png'
    else:
        output_file = input_file + '.png'
    
    # Process the data and create the plot
    pop_means = process_inbreeding_data(input_file)
    plot_inbreeding_coefficients(pop_means, output_file)

if __name__ == "__main__":
    main()
