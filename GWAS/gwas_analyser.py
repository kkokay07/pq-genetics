import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Tuple, List
import argparse
import sys

class GWASAnalyzer:
    def __init__(self, filepath: str = None, n_snps: int = None):
        """Initialize GWAS analyzer with input file path and number of SNPs."""
        if filepath is None:
            filepath = input("Enter the name of your .mlma file (with extension): ")
        
        self.trait_name = input("Enter the trait name: ")
        self.data = self.read_gwas_data(filepath)
        self.n_snps = n_snps if n_snps else len(self.data)
        self.lambda_gc = None
        
        # Standard GWAS thresholds
        self.significant_threshold = 5e-8
        self.suggestive_threshold = 1e-5
        
        # Calculate genomic inflation factor
        self.calculate_lambda()

    def read_gwas_data(self, filepath: str) -> pd.DataFrame:
        """Read and validate GCTA MLMA format results file."""
        try:
            # Read MLMA file
            df = pd.read_csv(filepath, delim_whitespace=True)
            
            # Check required columns
            required_columns = {'Chr', 'SNP', 'bp', 'A1', 'A2', 'Freq', 'b', 'se', 'p'}
            if not required_columns.issubset(df.columns):
                raise ValueError(f"Missing required columns. Required: {required_columns}")
            
            # Handle chromosome naming
            df['Chr'] = pd.to_numeric(df['Chr'], errors='coerce')
            
            # Convert p-values to -log10
            df['-log10p'] = -np.log10(df['p'])
            
            # Sort by p-value and save sorted results
            sorted_file = filepath.replace(".mlma", "_sorted_results.txt")
            df_sorted = df.sort_values('p')
            df_sorted.to_csv(sorted_file, sep='\t', index=False)
            print(f"\nRead {len(df)} SNPs from {filepath}")
            print(f"Sorted results saved to: {sorted_file}")
            
            # Print top 10 most significant SNPs
            print("\nTop 10 most significant SNPs:")
            print(df_sorted[['Chr', 'SNP', 'p', '-log10p', 'Freq', 'b']].head(10).to_string())
            
            return df
            
        except Exception as e:
            print(f"Error reading GWAS data: {e}")
            raise

    def calculate_lambda(self) -> float:
        """Calculate genomic inflation factor (λ)."""
        observed_chi2 = stats.chi2.ppf(1 - self.data['p'], 1)
        median_chi2 = np.median(observed_chi2)
        self.lambda_gc = median_chi2 / stats.chi2.ppf(0.5, 1)
        return self.lambda_gc

    def create_manhattan_plot(self, output_file: str = "manhattan_plot.png", dpi: int = 600):
        """Generate Manhattan plot with highlighted significant SNPs."""
        plt.figure(figsize=(15, 8))
        
        # Sort data by chromosome and position
        data = self.data.sort_values(['Chr', 'bp'])
        
        # Calculate cumulative position
        data['pos'] = 0
        offset = 0
        xticks = []
        
        # Process each chromosome
        for chrom in sorted(data['Chr'].unique()):
            chunk = data[data['Chr'] == chrom]
            data.loc[chunk.index, 'pos'] = chunk['bp'] + offset
            xticks.append(offset + (chunk['bp'].max() - chunk['bp'].min())/2)
            offset += chunk['bp'].max()
        
        # Plot points
        colors = ['#0073CF', '#FF8C00']
        for idx, chrom in enumerate(sorted(data['Chr'].unique())):
            chunk = data[data['Chr'] == chrom]
            
            # Plot all points
            plt.scatter(chunk['pos'], chunk['-log10p'], 
                       c=colors[idx % 2], s=2, alpha=0.7)
            
            # Highlight significant points with black circles
            sig_points = chunk[chunk['p'] < self.suggestive_threshold]
            if not sig_points.empty:
                plt.scatter(sig_points['pos'], sig_points['-log10p'],
                          facecolors='none', edgecolors='black', 
                          s=50, alpha=1, linewidth=1)
        
        # Add threshold lines without labels
        plt.axhline(y=-np.log10(self.significant_threshold), color='red', 
                   linestyle='--', alpha=0.5)
        plt.axhline(y=-np.log10(self.suggestive_threshold), color='blue', 
                   linestyle='--', alpha=0.5)
        
        # Customize plot
        plt.xlabel('Chromosome')
        plt.ylabel('-log10(p-value)')
        plt.xticks(xticks, sorted(data['Chr'].unique()))
        plt.title(f'{self.trait_name} Manhattan Plot (λ = {self.lambda_gc:.2f})')
        
        # Add grid
        plt.grid(True, alpha=0.1)
        
        # Save plot
        plt.tight_layout()
        plt.savefig(output_file, dpi=dpi)
        print(f"\nSaved Manhattan plot to: {output_file} (DPI: {dpi})")
        plt.close()

    def create_qq_plot(self, output_file: str = "qq_plot.png", dpi: int = 600):
        """Generate Q-Q plot of observed vs expected p-values."""
        plt.figure(figsize=(8, 8))
        
        # Calculate observed and expected p-values
        observed = -np.log10(np.sort(self.data['p']))
        expected = -np.log10(np.linspace(1/len(observed), 1, len(observed)))
        
        # Plot the diagonal line
        plt.plot([0, max(expected)], [0, max(expected)], 'r--', alpha=0.5)
        
        # Plot the Q-Q points
        plt.scatter(expected, observed, c='blue', s=2, alpha=0.5)
        
        # Customize plot
        plt.xlabel('Expected -log10(p)')
        plt.ylabel('Observed -log10(p)')
        plt.title(f'{self.trait_name} Q-Q Plot (λ = {self.lambda_gc:.2f})')
        
        # Add grid
        plt.grid(True, alpha=0.3)
        
        # Save plot
        plt.tight_layout()
        plt.savefig(output_file, dpi=dpi)
        print(f"\nSaved Q-Q plot to: {output_file} (DPI: {dpi})")
        plt.close()

    def save_significant_snps(self, output_file: str, threshold: float = 1e-4):
        """Save significant SNPs to a file."""
        significant = self.data[self.data['p'] < threshold].sort_values('p')
        significant.to_csv(output_file, index=False, sep='\t')
        print(f"\nSaved {len(significant)} significant SNPs to: {output_file}")

def main():
    if len(sys.argv) == 1:
        # Interactive mode
        analyzer = GWASAnalyzer()
        output_prefix = input("Enter output prefix for files (default: gwas_output): ") or "gwas_output"
        dpi = int(input("Enter DPI for plot (default: 600): ") or "600")
    else:
        # Command line mode
        parser = argparse.ArgumentParser(description='GWAS Analysis')
        parser.add_argument('input_file', help='Input MLMA file')
        parser.add_argument('--snps', type=int, help='Total number of SNPs analyzed')
        parser.add_argument('--out', default='gwas_output', help='Output prefix')
        parser.add_argument('--dpi', type=int, default=600, help='DPI for plot output')
        args = parser.parse_args()
        
        analyzer = GWASAnalyzer(args.input_file, args.snps)
        output_prefix = args.out
        dpi = args.dpi

    # Create plots and save results
    analyzer.create_manhattan_plot(f"{output_prefix}_manhattan.png", dpi=dpi)
    analyzer.create_qq_plot(f"{output_prefix}_qq.png", dpi=dpi)
    analyzer.save_significant_snps(f"{output_prefix}_significant_snps.txt")

if __name__ == "__main__":
    main()
