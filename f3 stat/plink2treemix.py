#!/usr/bin/env python3

import sys
import gzip
import argparse

def parse_args():
	parser = argparse.ArgumentParser(description='Convert PLINK .frq.strat file to TreeMix format')
	parser.add_argument('--freq', required=True, help='PLINK .frq.strat file')
	parser.add_argument('--out', required=True, help='Output filename (will be gzipped)')
	return parser.parse_args()

def read_freq_file(filename):
	"""Read PLINK .frq.strat file and return population data"""
	pops = set()
	snp_data = {}
    
	with open(filename) as f:
    	# Skip header line
    	header = f.readline()
   	 
    	# Process each line
    	for line in f:
        	fields = line.strip().split()
        	if len(fields) < 8:  # We need at least 8 fields
            	continue
       	 
        	try:
            	# Extract fields
            	snp = fields[1]
            	pop = fields[2]
            	mac = int(fields[6])   	# Minor allele count
            	nchrobs = int(fields[7])   # Number of chromosomes observed
           	 
            	# Calculate major allele count
            	mac_other = nchrobs - mac
           	 
            	# Add population to set
            	pops.add(pop)
           	 
            	# Store counts for this SNP and population
            	if snp not in snp_data:
                	snp_data[snp] = {}
           	 
            	if nchrobs > 0:
                	snp_data[snp][pop] = f"{mac_other},{mac}"
            	else:
                	snp_data[snp][pop] = "0,0"
               	 
        	except (ValueError, IndexError) as e:
            	print(f"Warning: Skipping line due to format error: {line.strip()}", file=sys.stderr)
            	continue
    
	return sorted(list(pops)), snp_data

def write_treemix(pops, snp_data, outfile):
	"""Write data in TreeMix format"""
	with gzip.open(outfile, 'wt') as f:
    	# Write header
    	f.write(' '.join(pops) + '\n')
   	 
    	# Write SNP data
    	valid_snps = 0
    	total_snps = 0
    	for snp in snp_data:
        	total_snps += 1
        	line = []
        	valid = True
       	 
        	# Check if we have data for all populations
        	for pop in pops:
            	if pop not in snp_data[snp]:
                	valid = False
                	break
            	counts = snp_data[snp][pop].split(',')
            	if sum(int(x) for x in counts) == 0:
                	valid = False
                	break
            	line.append(snp_data[snp][pop])
       	 
        	# Write line if valid
        	if valid:
            	f.write(' '.join(line) + '\n')
            	valid_snps += 1
   	 
    	print(f"Written {valid_snps} valid SNPs out of {total_snps} total SNPs", file=sys.stderr)

def main():
	args = parse_args()
    
	print("Reading frequency file...", file=sys.stderr)
	pops, snp_data = read_freq_file(args.freq)
    
	print(f"Found {len(pops)} populations:", file=sys.stderr)
	print(', '.join(pops), file=sys.stderr)
    
	print("\nWriting TreeMix file...", file=sys.stderr)
	write_treemix(pops, snp_data, args.out)
	print("\nConversion complete!", file=sys.stderr)

if __name__ == "__main__":
	main()
