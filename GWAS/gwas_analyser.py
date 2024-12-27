import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Tuple, List

class GWASAnalyzer:
    def __init__(self, filepath: str, n_snps: int = 53913):
        """Initialize GWAS analyzer with input file path and number of SNPs."""
        self.data = self.read_gwas_data(filepath)
        self.lambda_gc = None
        self.n_snps = n_snps
        
        # Standard GWAS thresholds
        self.significant_threshold = 5e-8  # Traditional genome-wide significance
        self.suggestive_threshold = 1e-5   # Traditional suggestive significance
        
        # Multiple testing corrected thresholds
        self.bonferroni_threshold = 0.05 / self.n_snps  # Bonferroni correction
        self.fdr_threshold = 0.05  # False Discovery Rate threshold
        
    def read_gwas_data(self, filepath: str) -> pd.DataFrame:
        """Read GCTA MLMA format results file.
        
        Expected columns in .mlma file:
        Chr: chromosome
        SNP: SNP identifier
        bp: base pair position
        A1: reference allele
        A2: alternate allele
        Freq: frequency of A1
        b: effect size
        se: standard error
        p: p-value
        """
        if not filepath.endswith('.mlma'):
            raise ValueError("Input file must be a GCTA MLMA format file (*.mlma)")
            
        try:
            # Read MLMA format file
            df = pd.read_csv(filepath, delim_whitespace=True)
            
            # Expected columns in MLMA format
            expected_columns = ['Chr', 'SNP', 'bp', 'A1', 'A2', 'Freq', 'b', 'se', 'p']
            
            # Check if all required columns are present
            missing_cols = [col for col in expected_columns if col not in df.columns]
            if missing_cols:
                raise ValueError(f"Missing required columns in MLMA file: {missing_cols}")
            
            # Standardize column names to match rest of script
            df = df.rename(columns={
                'Chr': 'CHR',
                'bp': 'POS',
                'p': 'P'
            })
            
            return df
        except Exception as e:
            print(f"Error reading GWAS data: {e}")
            raise

    def calculate_lambda(self) -> float:
        """Calculate genomic inflation factor (λ)."""
        observed_chi2 = stats.chi2.ppf(1 - self.data['P'], 1)
        median_chi2 = np.median(observed_chi2)
        self.lambda_gc = median_chi2 / stats.chi2.ppf(0.5, 1)
        return self.lambda_gc

    def create_manhattan_plot(self, output_file: str = "manhattan_plot.png"):
        """Generate Manhattan plot."""
        plt.figure(figsize=(12, 6))
        
        # Prepare data
        data = self.data.copy()
        data['-log10p'] = -np.log10(data['P'])
        
        # Alternate colors for chromosomes
        colors = ['#1f77b4', '#ff7f0e']
        unique_chromosomes = sorted(data['CHR'].unique())
        
        # Plot each chromosome
        x_offset = 0
        xticks = []
        for i, chrom in enumerate(unique_chromosomes):
            subset = data[data['CHR'] == chrom]
            pos = subset['POS'] + x_offset
            plt.scatter(pos, subset['-log10p'], 
                       c=colors[i % 2], 
                       s=1, 
                       alpha=0.7)
            xticks.append(x_offset + (max(subset['POS']) - min(subset['POS']))/2)
            x_offset += max(subset['POS'])
        
        # Add threshold lines
        plt.axhline(y=-np.log10(self.significant_threshold), color='red', linestyle='--', alpha=0.5)
        plt.axhline(y=-np.log10(self.suggestive_threshold), color='blue', linestyle='--', alpha=0.5)
        
        # Customize plot
        plt.xlabel('Chromosome')
        plt.ylabel('-log10(p-value)')
        plt.xticks(xticks, unique_chromosomes)
        plt.title(f'Manhattan Plot (λ = {self.lambda_gc:.2f})')
        
        # Save plot
        plt.tight_layout()
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        plt.close()

    def create_qq_plot(self, output_file: str = "qq_plot.png"):
        """Generate Q-Q plot."""
        # Calculate observed and expected p-values
        observed = -np.log10(sorted(self.data['P']))
        expected = -np.log10(np.linspace(0, 1, len(observed)+2)[1:-1])
        
        plt.figure(figsize=(6, 6))
        
        # Plot the diagonal line
        diagonal_line = np.linspace(0, max(max(observed), max(expected)), 100)
        plt.plot(diagonal_line, diagonal_line, 'r--', alpha=0.5)
        
        # Plot the actual data
        plt.scatter(expected, observed, c='#1f77b4', s=1, alpha=0.1)
        
        # Customize plot
        plt.xlabel('Expected -log10(p-value)')
        plt.ylabel('Observed -log10(p-value)')
        plt.title(f'Q-Q Plot (λ = {self.lambda_gc:.2f})')
        
        # Save plot
        plt.tight_layout()
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        plt.close()

    def calculate_fdr(self) -> pd.Series:
        """Calculate False Discovery Rate (Benjamini-Hochberg procedure)."""
        # Sort p-values
        sorted_df = self.data.sort_values('P')
        # Calculate FDR
        sorted_df['fdr'] = sorted_df['P'] * self.n_snps / sorted_df['P'].reset_index().index
        # Maintain monotonicity
        sorted_df['fdr'] = sorted_df['fdr'].cummin()
        return sorted_df.set_index(self.data.index)['fdr']

    def identify_associations(self) -> pd.DataFrame:
        """Identify associations using multiple significance criteria."""
        # Calculate FDR
        self.data['FDR'] = self.calculate_fdr()
        
        # Create copy of data for results
        results = self.data.copy()
        
        # Add columns for each significance criterion
        results['Significant_Traditional'] = results['P'] < self.significant_threshold
        results['Suggestive_Traditional'] = (results['P'] >= self.significant_threshold) & \
                                          (results['P'] < self.suggestive_threshold)
        results['Significant_Bonferroni'] = results['P'] < self.bonferroni_threshold
        results['Significant_FDR'] = results['FDR'] < self.fdr_threshold
        
        # Create overall significance category
        def get_significance_category(row):
            if row['Significant_Traditional']:
                return 'Genome-wide Significant (P < 5e-8)'
            elif row['Significant_Bonferroni']:
                return f'Bonferroni Significant (P < {self.bonferroni_threshold:.2e})'
            elif row['Significant_FDR']:
                return 'FDR Significant (FDR < 0.05)'
            elif row['Suggestive_Traditional']:
                return 'Suggestive (P < 1e-5)'
            else:
                return 'Not Significant'
        
        results['Significance_Category'] = results.apply(get_significance_category, axis=1)
        
        # Filter to keep only significant or suggestive results by any criterion
        significant_results = results[
            results['Significant_Traditional'] |
            results['Suggestive_Traditional'] |
            results['Significant_Bonferroni'] |
            results['Significant_FDR']
        ].copy()
        
        return significant_results

    def save_associations(self, output_file: str = "gwas_associations.csv"):
        """Save associations to CSV with multiple testing corrections."""
        # Get significant results with all criteria
        results = self.identify_associations()
        
        # Sort by chromosome and position
        results = results.sort_values(['CHR', 'POS'])
        
        # Save to CSV
        results.to_csv(output_file, index=False)
        
        return results

def main():
    # Parse command line arguments
    import argparse
    parser = argparse.ArgumentParser(description='GCTA MLMA Results Post-Processing Analysis')
    parser.add_argument('input_file', help='Input MLMA results file (must end in .mlma)')
    parser.add_argument('--out', default='gwas_output', help='Output prefix for files')
    parser.add_argument('--snps', type=int, default=53913, 
                       help='Total number of SNPs analyzed (default: 53913)')
    args = parser.parse_args()
    
    try:
        # Initialize analyzer
        analyzer = GWASAnalyzer(args.input_file, n_snps=args.snps)
        
        # Calculate lambda
        lambda_gc = analyzer.calculate_lambda()
        print(f"Genomic inflation factor (λ): {lambda_gc:.3f}")
        
        # Generate plots
        analyzer.create_manhattan_plot(f"{args.out}_manhattan.png")
        analyzer.create_qq_plot(f"{args.out}_qq.png")
        
        # Save associations
        results = analyzer.save_associations(f"{args.out}_associations.csv")
        
        # Print summary
        print("\nAnalysis Summary:")
        print(f"Total number of SNPs analyzed: {analyzer.n_snps}")
        print(f"Bonferroni significance threshold: {analyzer.bonferroni_threshold:.2e}")
        print("\nSignificant Associations:")
        print(f"- Traditional (P < 5e-8): {len(results[results['Significant_Traditional']])}")
        print(f"- Bonferroni (P < {analyzer.bonferroni_threshold:.2e}): {len(results[results['Significant_Bonferroni']])}")
        print(f"- FDR (FDR < 0.05): {len(results[results['Significant_FDR']])}")
        print(f"- Suggestive (P < 1e-5): {len(results[results['Suggestive_Traditional']])}")
        print(f"\nOutput files created:")
        print(f"- Manhattan plot: {args.out}_manhattan.png")
        print(f"- Q-Q plot: {args.out}_qq.png")
        print(f"- Associations: {args.out}_associations.csv")
        
    except Exception as e:
        print(f"Error during analysis: {e}")
        raise

if __name__ == "__main__":
    main()
