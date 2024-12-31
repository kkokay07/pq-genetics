import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import argparse

def calculate_heterozygosity(row):
    """Calculate observed and expected heterozygosity from PLINK .het output"""
    n_nm = row['N(NM)']
    o_hom = row['O(HOM)']
    e_hom = row['E(HOM)']
    
    # Calculate observed heterozygosity
    ho = (n_nm - o_hom) / n_nm
    
    # Calculate expected heterozygosity
    he = (n_nm - e_hom) / n_nm
    
    return pd.Series({'Ho': ho, 'He': he})

def prepare_population_data(df):
    """Extract population information and calculate mean metrics per population"""
    # Extract population from FID
    df['Population'] = df['FID'].apply(lambda x: x.split('_')[0])
    
    # Create separate dataframes for each metric, filtering negative values
    ho_df = df[df['Ho'] >= 0]
    he_df = df[df['He'] >= 0]
    fis_df = df[df['F'] >= 0]
    
    # Calculate statistics for each metric separately
    ho_stats = ho_df.groupby('Population')['Ho'].agg(['mean', 'std'])
    he_stats = he_df.groupby('Population')['He'].agg(['mean', 'std'])
    fis_stats = fis_df.groupby('Population')['F'].agg(['mean', 'std'])
    
    # Create a multi-level column structure for the final stats
    pop_stats = pd.concat({
        'Ho': ho_stats,
        'He': he_stats,
        'F': fis_stats
    }, axis=1)
    
    return pop_stats

def plot_population_heterozygosity(pop_stats, df, output_prefix, plot_title):
    """Create grouped bar plot for populations"""
    # Set figure size and DPI
    plt.figure(figsize=(12, 6), dpi=600)
    
    # Setup bar positions
    populations = pop_stats.index
    n_pop = len(populations)
    bar_width = 0.25
    positions = np.arange(n_pop)
    
    # Create bars
    plt.bar(positions - bar_width, pop_stats[('Ho', 'mean')], 
            bar_width, label='Ho', color='crimson', 
            yerr=pop_stats[('Ho', 'std')], capsize=5)
    plt.bar(positions, pop_stats[('He', 'mean')], 
            bar_width, label='He', color='royalblue', 
            yerr=pop_stats[('He', 'std')], capsize=5)
    plt.bar(positions + bar_width, pop_stats[('F', 'mean')], 
            bar_width, label='Fis', color='forestgreen', 
            yerr=pop_stats[('F', 'std')], capsize=5)
    
    # Customize plot
    plt.xlabel('Population')
    plt.ylabel('Value')
    if plot_title:
        plt.title(plot_title)
    plt.xticks(positions, populations, rotation=45)
    plt.legend()
    
    # Add grid
    plt.grid(True, axis='y', linestyle='--', alpha=0.7)
    plt.gca().set_axisbelow(True)
    
    # Adjust layout and save
    plt.tight_layout()
    plt.savefig(f'{output_prefix}_population_heterozygosity.png', bbox_inches='tight')
    plt.close()
    
    # Save summary statistics
    pop_stats.to_csv(f'{output_prefix}_population_stats.txt', sep='\t')
    
    # Save information about removed samples
    with open(f'{output_prefix}_removed_samples.txt', 'w') as f:
        f.write("Samples removed due to negative values:\n\n")
        f.write("For Ho calculation:\n")
        f.write(", ".join(df[df['Ho'] < 0]['FID'].tolist()) + "\n\n")
        f.write("For He calculation:\n")
        f.write(", ".join(df[df['He'] < 0]['FID'].tolist()) + "\n\n")
        f.write("For Fis calculation:\n")
        f.write(", ".join(df[df['F'] < 0]['FID'].tolist()) + "\n")

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Analyze PLINK heterozygosity output')
    parser.add_argument('het_file', help='Path to PLINK .het file')
    parser.add_argument('output_prefix', help='Prefix for output files')
    parser.add_argument('--title', help='Title for the plot', default=None)
    
    args = parser.parse_args()
    
    # Read the .het file
    df = pd.read_csv(args.het_file, sep='\s+')
    
    # Calculate heterozygosity metrics
    het_metrics = df.apply(calculate_heterozygosity, axis=1)
    df = pd.concat([df, het_metrics], axis=1)
    
    # Prepare population-wise statistics
    pop_stats = prepare_population_data(df)
    
    # Create population-wise plot
    plot_population_heterozygosity(pop_stats, df, args.output_prefix, args.title)
    
    print(f"Analysis complete. Output files saved with prefix: {args.output_prefix}")

if __name__ == "__main__":
    main()
