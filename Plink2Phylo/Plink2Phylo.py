#!/usr/bin/env python3

import os
import re
import numpy as np
import pandas as pd
import argparse
from scipy.cluster.hierarchy import linkage
from scipy.spatial.distance import squareform
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from io import StringIO

# Import ETE3 only for Tree data structure, not for rendering
try:
    from ete3 import Tree
except ImportError:
    print("Warning: ETE3 library not available. Using simple Newick parser.")
    # Simple Tree class as fallback
    class Tree:
        def __init__(self, newick_string=None):
            self.newick = newick_string
            self.leaves = []
            
        def write(self, format=1):
            return self.newick

def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description="Create a population-based phylogenetic tree from an individual-based distance matrix"
    )
    
    parser.add_argument("-d", "--dist", required=True,
                        help="Path to the distance matrix file (.mibs)")
    parser.add_argument("-i", "--ids", required=True,
                        help="Path to the IDs file (.mibs.id)")
    parser.add_argument("-p", "--pop", 
                        help="Path to the population assignment file (optional)")
    parser.add_argument("-o", "--output", default="population_tree",
                        help="Output prefix for generated files [default: population_tree]")
    parser.add_argument("-m", "--method", default="auto",
                        help="Method to extract populations: 'auto' (from ID prefix), 'file' (from file), or 'custom:X' (custom pattern) [default: auto]")
    parser.add_argument("--pattern", default="^[A-Z]+",
                        help="Regex pattern to extract populations when using auto method [default: ^[A-Z]+]")
    parser.add_argument("--min-samples", type=int, default=1,
                        help="Minimum samples required per population to include in analysis [default: 1]")
    parser.add_argument("--no-plots", action="store_true",
                        help="Skip creating plot PDF files")
    
    return parser.parse_args()

def extract_population(id_str, pattern="^[A-Z]+"):
    """Extract population identifier from individual ID"""
    pop_match = re.search(pattern, id_str)
    if pop_match and pop_match.group(0):
        return pop_match.group(0)
    else:
        # Fallback: use first three characters
        return id_str[:3]

def calculate_pop_distance(pop1, pop2, dist_matrix, pop_assignments):
    """Calculate average distance between two populations"""
    # Get individuals from each population
    inds_pop1 = pop_assignments[pop_assignments['population'] == pop1]['individual'].values
    inds_pop2 = pop_assignments[pop_assignments['population'] == pop2]['individual'].values
    
    # Calculate pairwise distances
    distances = []
    for ind1 in inds_pop1:
        for ind2 in inds_pop2:
            if ind1 != ind2:  # Skip same individual comparisons
                if ind1 in dist_matrix.index and ind2 in dist_matrix.columns:
                    distances.append(dist_matrix.loc[ind1, ind2])
    
    # Return mean distance (or 0 if no valid comparisons)
    if distances:
        return np.mean(distances)
    else:
        return 0

def build_neighbor_joining_tree(dist_matrix):
    """Build a neighbor-joining tree from a distance matrix"""
    # Ensure diagonal is zero
    np.fill_diagonal(dist_matrix.values, 0)
    
    # Make sure the matrix is symmetric
    dist_matrix_sym = (dist_matrix + dist_matrix.T) / 2
    
    # Convert to condensed distance matrix
    condensed_dist = squareform(dist_matrix_sym)
    
    # Use UPGMA for clustering (scipy doesn't have direct NJ)
    # This is an approximation - for exact NJ, we'd need Bio.Phylo
    tree_matrix = linkage(condensed_dist, method='average')
    
    # Convert to Newick format using ETE3
    # This is a simplified approach - for production, consider using Bio.Phylo
    tree_string = construct_newick_from_linkage(tree_matrix, dist_matrix.index)
    
    return Tree(tree_string)

def construct_newick_from_linkage(linkage_matrix, labels):
    """Construct a Newick tree string from scipy linkage matrix"""
    n = len(labels)
    nodes = [f"{label}" for label in labels]
    
    for i, (a, b, dist, count) in enumerate(linkage_matrix):
        a, b = int(a), int(b)
        new_node = f"({nodes[a]},{nodes[b]}):{dist/2}"
        nodes.append(new_node)
    
    return nodes[-1] + ";"

def main():
    args = parse_arguments()
    
    print("=== Population Tree Generation ===")
    print(f"Distance matrix file: {args.dist}")
    print(f"IDs file: {args.ids}")
    print(f"Output prefix: {args.output}")
    print(f"Population method: {args.method}")
    print()
    
    # Read input files
    print("Reading input files...")
    ids = pd.read_csv(args.ids, sep='\t', header=None)
    dist_matrix = pd.read_csv(args.dist, sep='\t', header=None)
    
    # Set row and column names
    dist_matrix.index = ids[0]
    dist_matrix.columns = ids[0]
    
    # Process population assignments
    print("Processing population assignments...")
    if args.method == "file" and args.pop is not None:
        # Read from file
        print(f"Reading population assignments from file: {args.pop}")
        pop_data = pd.read_csv(args.pop, sep='\t', header=None)
        if pop_data.shape[1] >= 2:
            population_assignments = pd.DataFrame({
                'individual': pop_data.iloc[:, 1],  # Assuming second column is individual ID
                'population': pop_data.iloc[:, 0]   # Assuming first column is population ID
            })
        else:
            raise ValueError("Population file must have at least 2 columns.")
    elif args.method.startswith("custom:"):
        # Use custom regex pattern
        custom_pattern = args.method.replace("custom:", "")
        print(f"Using custom pattern for population extraction: {custom_pattern}")
        populations = [extract_population(id_str, custom_pattern) for id_str in ids[0]]
        population_assignments = pd.DataFrame({
            'individual': ids[0],
            'population': populations
        })
    else:
        # Auto method (default)
        print(f"Extracting populations automatically using pattern: {args.pattern}")
        populations = [extract_population(id_str, args.pattern) for id_str in ids[0]]
        population_assignments = pd.DataFrame({
            'individual': ids[0],
            'population': populations
        })
    
    # Check for missing assignments and report
    missing_pops = set(ids[0]) - set(population_assignments['individual'])
    if missing_pops:
        print(f"Warning: Missing population assignments for {len(missing_pops)} individuals")
        print(f"First few missing IDs: {list(missing_pops)[:5]}")
        
        # Create assignments for missing individuals based on ID prefix
        new_assignments = pd.DataFrame({
            'individual': list(missing_pops),
            'population': [extract_population(id_str, args.pattern) for id_str in missing_pops]
        })
        population_assignments = pd.concat([population_assignments, new_assignments], ignore_index=True)
        print("Created automatic assignments for missing individuals.")
    
    # Filter small populations if requested
    pop_counts = population_assignments['population'].value_counts()
    print(f"Found {len(pop_counts)} populations with sample sizes:")
    print(pop_counts)
    
    if args.min_samples > 1:
        small_pops = pop_counts[pop_counts < args.min_samples].index.tolist()
        if small_pops:
            print(f"\nWarning: {len(small_pops)} populations have fewer than {args.min_samples} samples:")
            print(small_pops)
            print(f"These will be excluded from the population-level analysis.")
            
            # Remove small populations
            population_assignments = population_assignments[
                ~population_assignments['population'].isin(small_pops)
            ]
            print(f"After filtering: {len(population_assignments['population'].unique())} populations remain.")
    
    # Make sure output directory exists
    os.makedirs(os.path.dirname(args.output) if os.path.dirname(args.output) else '.', exist_ok=True)
    
    # Build individual-based tree
    print("Building individual-based tree...")
    individual_tree = build_neighbor_joining_tree(dist_matrix)
    
    # Save individual tree in Newick format
    individual_tree_file = f"{args.output}_individual.newick"
    individual_tree.write(outfile=individual_tree_file, format=1)  # format=1 is Newick
    print(f"Individual tree saved to: {individual_tree_file}")
    
    # Plot tree if requested
    if not args.no_plots:
        # Write tree to text file instead of PDF
        newick_str = individual_tree.write(format=1)
        
        # Save as text file
        with open(f"{args.output}_individual.txt", "w") as f:
            f.write("Individual-Based Neighbor-Joining Tree\n\n")
            f.write(newick_str)
        
        print(f"Individual tree info saved to: {args.output}_individual.txt")
    
    # Create population-level distance matrix
    print("Building population-based tree...")
    pop_names = population_assignments['population'].unique()
    pop_dist_matrix = pd.DataFrame(
        np.zeros((len(pop_names), len(pop_names))),
        index=pop_names,
        columns=pop_names
    )
    
    # Fill the population distance matrix
    print("Calculating population distances...")
    for i, pop1 in enumerate(pop_names):
        for j, pop2 in enumerate(pop_names[i:], i):
            if pop1 != pop2:
                dist_val = calculate_pop_distance(
                    pop1, pop2, 
                    dist_matrix, population_assignments
                )
                pop_dist_matrix.loc[pop1, pop2] = dist_val
                pop_dist_matrix.loc[pop2, pop1] = dist_val  # Matrix is symmetric
        
        # Show progress
        if (i + 1) % 5 == 0 or i + 1 == len(pop_names):
            print(f"Progress: {i + 1} of {len(pop_names)} populations processed")
    
    # Build NJ tree for populations
    pop_tree = build_neighbor_joining_tree(pop_dist_matrix)
    
    # Save population-based tree in Newick format
    pop_tree_file = f"{args.output}_population.newick"
    pop_tree.write(outfile=pop_tree_file, format=1)
    print(f"Population-based tree saved to: {pop_tree_file}")
    
    # Plot population-based tree
    if not args.no_plots:
        # Save population tree as text file
        newick_str = pop_tree.write(format=1)
        with open(f"{args.output}_population.txt", "w") as f:
            f.write("Population-Based Neighbor-Joining Tree\n\n")
            f.write(newick_str)
        print(f"Population tree info saved to: {args.output}_population.txt")
        
        # Create a simple text representation of the colored tree
        with open(f"{args.output}_individual_colored.txt", "w") as f:
            f.write("Individual Tree with Tips Colored by Population\n\n")
            
            # Prepare population info
            unique_pops = population_assignments['population'].unique()
            f.write("Populations:\n")
            for pop in unique_pops:
                count = len(population_assignments[population_assignments['population'] == pop])
                f.write(f"- {pop}: {count} individuals\n")
            
            f.write("\nTree structure:\n")
            f.write(individual_tree.write(format=1))
        
        print(f"Colored individual tree info saved to: {args.output}_individual_colored.txt")
    
    # Print summary information
    print("\n=== Summary ===")
    print(f"Total individuals: {len(ids)}")
    print(f"Populations in final tree: {len(pop_names)}")
    print("\nOutput files created:")
    print(f"- {args.output}_individual.newick (Individual tree)")
    print(f"- {args.output}_population.newick (Population tree)")
    if not args.no_plots:
        print(f"- {args.output}_individual.txt (Individual tree info)")
        print(f"- {args.output}_population.txt (Population tree info)")
        print(f"- {args.output}_individual_colored.txt (Individual tree with populations info)")
    
    print("\nAnalysis complete.")

if __name__ == "__main__":
    main()
