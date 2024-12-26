import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from argparse import ArgumentParser

def create_feature_barplot(input_file, output_file):
    # Read the TSV file
    df = pd.read_csv(input_file, sep='\t')
    
    # Get feature counts
    feature_counts = df['feature_type'].value_counts()
    
    # Set the style using seaborn
    sns.set_style("whitegrid")
    
    # Create figure and axis with specific size
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Create color palette
    colors = sns.color_palette("Set2", len(feature_counts))
    
    # Create barplot
    bars = ax.bar(range(len(feature_counts)), 
                  feature_counts.values,
                  color=colors)
    
    # Customize the plot
    ax.set_title('Distribution of Genomic Features\n' + 
                 f'Region: {df.iloc[0]["region_chr"]}:{df.iloc[0]["region_start"]}-{df.iloc[0]["region_end"]}', 
                 fontsize=16, 
                 pad=20,
                 fontweight='bold')
    ax.set_xlabel('Feature Type', fontsize=12, labelpad=10)
    ax.set_ylabel('Count', fontsize=12, labelpad=10)
    
    # Set x-axis ticks
    ax.set_xticks(range(len(feature_counts)))
    ax.set_xticklabels(feature_counts.index, 
                       rotation=45, 
                       ha='right',
                       fontsize=10)
    
    # Add value labels on top of each bar
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., 
                height,
                f'{int(height)}',
                ha='center', 
                va='bottom',
                fontsize=10)
    
    # Remove top and right spines
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    # Adjust layout to prevent label cutoff
    plt.tight_layout()
    
    # Save with high DPI
    plt.savefig(output_file, dpi=600, bbox_inches='tight')
    print(f"Plot saved as {output_file}")
    
    # Print feature counts
    print("\nFeature counts:")
    for feature, count in feature_counts.items():
        print(f"{feature}: {count}")

def main():
    parser = ArgumentParser(description='Create feature distribution barplot')
    parser.add_argument('--input', required=True, help='Input TSV file with feature annotations')
    parser.add_argument('--output', required=True, help='Output image file (e.g., features_plot.png)')
    
    args = parser.parse_args()
    
    # Create the plot
    create_feature_barplot(args.input, args.output)

if __name__ == "__main__":
    main()
