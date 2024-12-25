import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Ellipse
from scipy.stats import chi2
import argparse

def get_confidence_ellipse(x, y, confidence=0.95):
    if len(x) < 3:
        return None, None, None
    
    cov = np.cov(x, y)
    pearson = cov[0, 1]/np.sqrt(cov[0, 0] * cov[1, 1])
    chi2_val = chi2.ppf(confidence, 2)
    eigenvals, eigenvecs = np.linalg.eig(cov)
    
    sort_indices = np.argsort(eigenvals)[::-1]
    eigenvals = eigenvals[sort_indices]
    eigenvecs = eigenvecs[:,sort_indices]
    
    angle = np.degrees(np.arctan2(eigenvecs[1,0], eigenvecs[0,0]))
    width, height = 2 * np.sqrt(chi2_val * eigenvals)
    
    return width, height, angle

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='PCA Visualization Tool')
    parser.add_argument('--eigenvec', required=True, help='Path to eigenvector file')
    parser.add_argument('--eigenval', required=True, help='Path to eigenvalue file')
    parser.add_argument('--fam', required=True, help='Path to fam file')
    parser.add_argument('--ellipse-pops', nargs='+', help='Populations to draw confidence ellipses for')
    parser.add_argument('--dpi', type=int, default=600, help='DPI for output images')
    args = parser.parse_args()

    # Read the files
    eigenvec = pd.read_table(args.eigenvec, sep=r'\s+', header=None)
    eigenval = pd.read_table(args.eigenval, sep=r'\s+', header=None)
    fam = pd.read_table(args.fam, sep=r'\s+', header=None)

    # Rename columns
    eigenvec.columns = ['FID', 'IID'] + [f'PC{i+1}' for i in range(eigenvec.shape[1]-2)]
    eigenvec['Population'] = fam[0]

    # Calculate variance explained
    total_variance = eigenval[0].sum()
    variance_explained = (eigenval[0] / total_variance) * 100
    cumulative_variance = np.cumsum(variance_explained)

    # Define markers and colors for different populations
    markers = ['*', '+', 'x', 'D', 's', '^', 'v', '<', '>', 'p', 'h']  # More distinct shapes
    colors = ['#e41a1c', '#377eb8', '#4daf4a', '#984ea3', '#ff7f00', 
              '#d62728', '#2ca02c', '#9467bd', '#8c564b', '#e377c2', '#1f77b4']  # No light colors
    
    populations = eigenvec['Population'].unique()
    pop_style = {pop: {'marker': markers[i % len(markers)], 
                      'color': colors[i % len(colors)]} 
                 for i, pop in enumerate(populations)}

    # Create PC1 vs PC2 plot
    plt.figure(figsize=(12, 8))
    for pop in populations:
        mask = eigenvec['Population'] == pop
        pop_data = eigenvec[mask]
        
        # Plot points with specific marker and color
        plt.scatter(pop_data['PC1'], pop_data['PC2'],
                   marker=pop_style[pop]['marker'],
                   c=pop_style[pop]['color'],
                   label=pop,
                   alpha=0.7,
                   s=100)
        
        # Add ellipse if population is in ellipse_pops
        if args.ellipse_pops and pop in args.ellipse_pops:
            width, height, angle = get_confidence_ellipse(pop_data['PC1'], pop_data['PC2'])
            if width is not None:
                ellipse = Ellipse(xy=(pop_data['PC1'].mean(), pop_data['PC2'].mean()),
                                width=width, height=height, angle=angle,
                                fill=False, color=pop_style[pop]['color'], alpha=0.5)
                plt.gca().add_patch(ellipse)

    plt.xlabel(f'PC1 ({variance_explained[0]:.2f}%)')
    plt.ylabel(f'PC2 ({variance_explained[1]:.2f}%)')
    plt.title('PC1 vs PC2')

    plt.legend(bbox_to_anchor=(1.05, 1),
              loc='upper left',
              title="Population",
              fontsize=10,
              title_fontsize=12,
              borderaxespad=0,
              frameon=True,
              edgecolor='black',
              fancybox=True,
              shadow=True)

    plt.tight_layout()
    plt.savefig('pca_pc1_vs_pc2.png', dpi=args.dpi, bbox_inches='tight')
    plt.close()

    # Create similar plots for PC3 vs PC4
    plt.figure(figsize=(12, 8))
    for pop in populations:
        mask = eigenvec['Population'] == pop
        pop_data = eigenvec[mask]
        
        plt.scatter(pop_data['PC3'], pop_data['PC4'],
                   marker=pop_style[pop]['marker'],
                   c=pop_style[pop]['color'],
                   label=pop,
                   alpha=0.7,
                   s=100)
        
        if args.ellipse_pops and pop in args.ellipse_pops:
            width, height, angle = get_confidence_ellipse(pop_data['PC3'], pop_data['PC4'])
            if width is not None:
                ellipse = Ellipse(xy=(pop_data['PC3'].mean(), pop_data['PC4'].mean()),
                                width=width, height=height, angle=angle,
                                fill=False, color=pop_style[pop]['color'], alpha=0.5)
                plt.gca().add_patch(ellipse)

    plt.xlabel(f'PC3 ({variance_explained[2]:.2f}%)')
    plt.ylabel(f'PC4 ({variance_explained[3]:.2f}%)')
    plt.title('PC3 vs PC4')

    plt.legend(bbox_to_anchor=(1.05, 1),
              loc='upper left',
              title="Population",
              fontsize=10,
              title_fontsize=12,
              borderaxespad=0,
              frameon=True,
              edgecolor='black',
              fancybox=True,
              shadow=True)

    plt.tight_layout()
    plt.savefig('pca_pc3_vs_pc4.png', dpi=args.dpi, bbox_inches='tight')
    plt.close()

    # Create variance plots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

    pc_range = range(1, 21)
    ax1.bar(pc_range, variance_explained[:20], alpha=0.8)
    ax1.plot(pc_range, variance_explained[:20], 'r-', linewidth=2)
    ax1.set_xlabel('Principal Component')
    ax1.set_ylabel('Variance Explained (%)')
    ax1.set_title('Scree Plot')
    ax1.set_xticks(pc_range)
    ax1.grid(True, linestyle='--', alpha=0.3)

    ax2.plot(pc_range, cumulative_variance[:20], 'b-', linewidth=2, marker='o')
    ax2.set_xlabel('Principal Component')
    ax2.set_ylabel('Cumulative Variance Explained (%)')
    ax2.set_title('Cumulative Variance Explained')
    ax2.set_xticks(pc_range)
    ax2.axhline(y=80, color='r', linestyle='--', alpha=0.5, label='80%')
    ax2.axhline(y=90, color='r', linestyle='--', alpha=0.5, label='90%')
    ax2.grid(True, linestyle='--', alpha=0.3)
    ax2.legend()

    plt.tight_layout()
    plt.savefig('pca_variance_plots.png', dpi=args.dpi, bbox_inches='tight')
    plt.close()

    # Print summary statistics
    print("\nVariance explained by first 10 PCs:")
    for i in range(10):
        print(f"PC{i+1}: {variance_explained[i]:.2f}% (Cumulative: {cumulative_variance[i]:.2f}%)")

    print("\nSamples per population:")
    print(eigenvec['Population'].value_counts())

if __name__ == "__main__":
    main()
