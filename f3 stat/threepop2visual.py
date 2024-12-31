import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def parse_f3_results(file_path):
	"""Parse f3 statistics results file into a pandas DataFrame."""
	data = []
	with open(file_path, 'r') as f:
    	for line in f:
        	if ';' in line:  # Only process lines containing f3 results
            	parts = line.strip().split()
            	populations = parts[0].split(';')
            	target = populations[0]
            	source1, source2 = populations[1].split(',')
            	f3_stat = float(parts[1])
            	std_err = float(parts[2])
            	z_score = float(parts[3])
           	 
            	data.append({
                	'target': target,
                	'source1': source1,
                	'source2': source2,
                	'f3': f3_stat,
                	'stderr': std_err,
                	'z_score': z_score,
                	'label': f"{target};{source1},{source2}"
            	})
    
	return pd.DataFrame(data)

def plot_f3_statistics_centered(df, output_file=None, figsize=(12, 20)):
	"""Create a horizontal bar plot of f3 statistics with centered y-axis."""
	# Sort by absolute Z-score
	df['abs_z'] = abs(df['z_score'])
	df_sorted = df.sort_values('abs_z', ascending=True)
    
	# Create figure
	fig, ax = plt.subplots(figsize=figsize)
    
	# Create color palette based on z-score signs
	colors = ['#FF7F7F' if z < 0 else '#66C2A5' for z in df_sorted['z_score']]
    
	# Create horizontal bar plot
	bars = ax.barh(range(len(df_sorted)),
              	df_sorted['f3'],
              	xerr=df_sorted['stderr'],
              	color=colors,
              	capsize=3)
    
	# Find the maximum absolute value for x-axis symmetry
	max_abs_x = max(abs(df_sorted['f3'].max()), abs(df_sorted['f3'].min()))
	plt.xlim(-max_abs_x * 1.2, max_abs_x * 1.2)
    
	# Add vertical line at x=0
	ax.axvline(x=0, color='black', linestyle='-', linewidth=0.5)
    
	# Remove y-axis labels initially
	ax.set_yticks([])
    
	# Add labels and Z-scores at the end of bars
	for idx, row in enumerate(df_sorted.itertuples()):
    	# Determine text color and position based on f3 value
    	if row.f3 < 0:
        	x_pos = row.f3 - row.stderr * 1.5
        	ha = 'right'
    	else:
        	x_pos = row.f3 + row.stderr * 1.5
        	ha = 'left'
       	 
    	# Add population labels
    	ax.text(0, idx, row.label,
            	ha='center', va='center',
            	bbox=dict(facecolor='white', edgecolor='none', alpha=0.7))
   	 
    	# Add Z-score
    	ax.text(x_pos, idx, f'Z: {row.z_score:.2f}',
            	ha=ha, va='center',
            	bbox=dict(facecolor='white', edgecolor='none', alpha=0.7))
    
	# Customize plot
	ax.set_xlabel('Three population statistics (f3)')
	ax.set_title('Three population tests')
    
	# Add gridlines
	ax.grid(True, axis='x', linestyle='--', alpha=0.3)
    
	# Adjust layout
	plt.tight_layout()
    
	# Save if output file is specified
	if output_file:
    	plt.savefig(output_file, dpi=300, bbox_inches='tight')
   	 
	return fig

# Example usage
if __name__ == "__main__":
	# Read and parse the f3 results
	df = parse_f3_results('f3_results.txt')
    
	# Create the plot and save it
	plot_f3_statistics_centered(df, output_file='f3_statistics_centered.png')
