import subprocess
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import argparse
import sys
import numpy as np

class RegionAnnotator:
    def __init__(self, input_file, gff_file, output_prefix, trait_name):
        """Initialize the region annotator with input files, output prefix and trait name."""
        self.input_file = input_file
        self.gff_file = gff_file
        self.output_prefix = output_prefix
        self.trait_name = trait_name
        self.intersect_results = None
        
    def read_input_regions(self):
        """Read and validate input regions file."""
        try:
            regions = pd.read_csv(self.input_file, sep='\t')
            required_cols = {'CHR', 'START', 'END'}
            if not required_cols.issubset(regions.columns):
                raise ValueError(f"Input file must contain columns: {required_cols}")
            return regions
        except Exception as e:
            print(f"Error reading input file: {e}")
            return None

    def create_bed(self, regions_df):
        """Create BED format file from input regions."""
        bed_file = f"{self.output_prefix}.bed"
        bed_df = regions_df.copy()
        bed_df['name'] = bed_df.apply(lambda x: f"{x['CHR']}_{x['START']}_{x['END']}", axis=1)
        bed_df[['CHR', 'START', 'END', 'name']].to_csv(
            bed_file, sep='\t', header=False, index=False
        )
        return bed_file

    def run_bedtools_intersection(self):
        """Run bedtools to intersect regions with GFF features."""
        try:
            regions_df = self.read_input_regions()
            if regions_df is None:
                return False

            bed_file = self.create_bed(regions_df)
            
            cmd = [
                'bedtools', 'intersect',
                '-a', bed_file,
                '-b', self.gff_file,
                '-wa', '-wb'
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            
            intersections = []
            for line in result.stdout.strip().split('\n'):
                if line:
                    fields = line.split('\t')
                    if len(fields) >= 12:
                        intersection = {
                            'region_chr': fields[0],
                            'region_start': int(fields[1]),
                            'region_end': int(fields[2]),
                            'feature_chr': fields[4],
                            'feature_source': fields[5],
                            'feature_type': fields[6],
                            'feature_start': int(fields[7]),
                            'feature_end': int(fields[8]),
                            'feature_strand': fields[9],
                            'feature_attributes': fields[11]
                        }
                        intersections.append(intersection)
            
            self.intersect_results = pd.DataFrame(intersections)
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"Error running bedtools: {e}")
            print(f"stderr: {e.stderr}")
            return False
        except Exception as e:
            print(f"Error processing intersection: {e}")
            return False

    def create_summary_plots(self, dpi=600):
        """Create summary plots of the intersection results."""
        if self.intersect_results is None or self.intersect_results.empty:
            print("No results to plot")
            return

        # Set figure style
        plt.rcParams['figure.autolayout'] = True
        
        # Set default style settings for better visualization
        plt.rcParams['axes.grid'] = True
        plt.rcParams['grid.alpha'] = 0.3
        plt.rcParams['axes.facecolor'] = 'white'
        plt.rcParams['figure.facecolor'] = 'white'
        
        # Color palette
        colors = ['#2ecc71', '#3498db', '#e74c3c', '#f1c40f', '#9b59b6', 
                 '#1abc9c', '#e67e22', '#34495e', '#7f8c8d', '#2c3e50']
        
        # 1. Feature Type Distribution (Pie Chart)
        plt.figure(figsize=(10, 8))
        feature_counts = self.intersect_results['feature_type'].value_counts()
        plt.pie(feature_counts, labels=feature_counts.index, 
                autopct='%1.1f%%', colors=colors[:len(feature_counts)])
        plt.title(f'{self.trait_name} Related Feature Type Distribution', pad=20, size=12)
        plt.savefig(f"{self.output_prefix}_feature_types_pie.png", 
                    dpi=dpi, bbox_inches='tight')
        plt.close()

        # 2. Feature Type Distribution (Bar Plot)
        plt.figure(figsize=(12, 6))
        x = np.arange(len(feature_counts))
        plt.bar(x, feature_counts.values, color=colors[:len(feature_counts)])
        plt.xticks(x, feature_counts.index, rotation=45, ha='right')
        plt.title(f'{self.trait_name} Related Feature Types Distribution', pad=20, size=12)
        plt.xlabel('Feature Type', size=10)
        plt.ylabel('Count', size=10)
        plt.grid(True, alpha=0.3)
        plt.savefig(f"{self.output_prefix}_feature_types_bar.png", 
                    dpi=dpi, bbox_inches='tight')
        plt.close()

        # 3. Region Distribution
        plt.figure(figsize=(12, 6))
        region_counts = self.intersect_results.groupby('region_chr').size()
        x = np.arange(len(region_counts))
        plt.bar(x, region_counts.values, color=colors[:len(region_counts)])
        plt.xticks(x, region_counts.index, rotation=45)
        plt.title(f'{self.trait_name} Related Feature Distribution in Different Chromosomes', 
                 pad=20, size=12)
        plt.xlabel('Chromosome', size=10)
        plt.ylabel('Number of Features', size=10)
        plt.grid(True, alpha=0.3)
        plt.savefig(f"{self.output_prefix}_region_distribution.png", 
                    dpi=dpi, bbox_inches='tight')
        plt.close()

def main():
    parser = argparse.ArgumentParser(description='Region Feature Annotation Tool')
    parser.add_argument('--input', required=True, help='Input regions file (CHR, START, END)')
    parser.add_argument('--gff', required=True, help='Reference GFF file')
    parser.add_argument('--output', required=True, help='Output prefix')
    parser.add_argument('--trait', required=True, help='Name of the trait being analyzed')
    parser.add_argument('--dpi', type=int, default=600, help='DPI for plots')
    
    args = parser.parse_args()
    
    annotator = RegionAnnotator(args.input, args.gff, args.output, args.trait)
    
    # Run intersection
    print("Running bedtools intersection...")
    if not annotator.run_bedtools_intersection():
        sys.exit(1)
    
    # Create visualizations
    print("Creating summary plots...")
    annotator.create_summary_plots(dpi=args.dpi)
    
    print(f"\nAnalysis complete. Results saved with prefix: {args.output}")

if __name__ == "__main__":
    main()
