#!/usr/bin/env python3
import argparse
import sys
import numpy as np

def read_phenotype_data(filename):
    """Read phenotype data file and return dictionary of traits"""
    traits = {}
    try:
        with open(filename, 'r') as f:
            # Read and process header if it exists
            first_line = f.readline().strip().split()
            
            # Check if first line is header or data
            if any(not is_numeric(val) for val in first_line[2:]):  # Assuming FID/IID in first two columns
                headers = first_line[2:]  # Skip FID/IID columns
                start_idx = 0
            else:
                # If no header, use column numbers as trait names
                headers = [f"Trait_{i}" for i in range(1, len(first_line)-1)]
                start_idx = -1  # To trigger file reread
            
            # Initialize traits dictionary
            for h in headers:
                traits[h] = []
            
            # Reset file if no header was found
            if start_idx == -1:
                f.seek(0)
                
            # Read data
            for line in f:
                values = line.strip().split()
                # Skip FID/IID columns (first two columns)
                for header, value in zip(headers, values[2:]):
                    if is_numeric(value):
                        traits[header].append(float(value))
                    
    except Exception as e:
        print(f"Error reading file: {str(e)}")
        sys.exit(1)
        
    return traits

def is_numeric(value):
    """Check if a string can be converted to float"""
    try:
        float(value)
        return True
    except ValueError:
        return False

def calculate_statistics(values):
    """Calculate comprehensive statistics for a trait"""
    values = [v for v in values if v != -9 and v != -999]  # Remove common missing value codes
    n = len(values)
    if n == 0:
        return None
    
    # Convert to numpy array for efficient calculations
    values = np.array(values)
    
    # Calculate statistics
    stats = {
        'n': n,
        'mean': np.mean(values),
        'median': np.median(values),
        'std_dev': np.std(values, ddof=1),
        'min': np.min(values),
        'max': np.max(values),
        'q1': np.percentile(values, 25),
        'q3': np.percentile(values, 75),
        'skewness': calculate_skewness(values),
        'kurtosis': calculate_kurtosis(values),
        'missing': len([v for v in values if v == -9 or v == -999])
    }
    
    stats['iqr'] = stats['q3'] - stats['q1']
    return stats

def calculate_skewness(values):
    """Calculate skewness of distribution"""
    n = len(values)
    if n < 3:
        return None
    m3 = np.mean((values - np.mean(values))**3)
    m2 = np.mean((values - np.mean(values))**2)
    return m3 / (m2**1.5)

def calculate_kurtosis(values):
    """Calculate kurtosis of distribution"""
    n = len(values)
    if n < 4:
        return None
    m4 = np.mean((values - np.mean(values))**4)
    m2 = np.mean((values - np.mean(values))**2)
    return m4 / (m2**2) - 3  # Excess kurtosis

def describe_distribution(stats):
    """Return a description of the distribution shape"""
    if stats['skewness'] is None:
        return "Not enough data to determine distribution shape"
    
    description = []
    
    # Check skewness
    if abs(stats['skewness']) > 0.5:
        direction = "positively" if stats['skewness'] > 0 else "negatively"
        description.append(f"Distribution is {direction} skewed")
    else:
        description.append("Distribution is approximately symmetric")
    
    # Check kurtosis
    if stats['kurtosis'] is not None:
        if stats['kurtosis'] > 0.5:
            description.append("with heavy tails")
        elif stats['kurtosis'] < -0.5:
            description.append("with light tails")
    
    return " ".join(description)

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Analyze phenotype data distribution')
    parser.add_argument('phenotype_file', help='Input phenotype file (FID IID pheno1 pheno2 ...)')
    parser.add_argument('--out', help='Output file prefix', default='pheno_distribution')
    args = parser.parse_args()
    
    # Read data
    print(f"Reading phenotype data from {args.phenotype_file}...")
    traits = read_phenotype_data(args.phenotype_file)
    
    # Open output file
    with open(f"{args.out}.txt", 'w') as out_f:
        # Analyze each trait
        for trait_name, values in traits.items():
            stats = calculate_statistics(values)
            if not stats:
                print(f"Warning: No valid data for trait {trait_name}")
                continue
            
            # Prepare output
            output = [
                f"\nDistribution Analysis for {trait_name}",
                "-" * 40,
                f"Number of observations: {stats['n']}",
                f"Mean: {stats['mean']:.2f}",
                f"Median: {stats['median']:.2f}",
                f"Standard deviation: {stats['std_dev']:.2f}",
                f"Minimum: {stats['min']:.2f}",
                f"Maximum: {stats['max']:.2f}",
                f"First quartile (Q1): {stats['q1']:.2f}",
                f"Third quartile (Q3): {stats['q3']:.2f}",
                f"Interquartile range (IQR): {stats['iqr']:.2f}",
                f"Skewness: {stats['skewness']:.3f}",
                f"Kurtosis: {stats['kurtosis']:.3f}",
                describe_distribution(stats),
                f"Missing values: {stats['missing']}"
            ]
            
            # Print to both console and file
            print("\n".join(output))
            print("\n".join(output), file=out_f)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nAnalysis interrupted by user")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        sys.exit(1)
