import pandas as pd
import subprocess
from argparse import ArgumentParser

def parse_attributes(attr_string):
    """Parse GFF attributes into a dictionary"""
    attrs = {}
    for item in attr_string.split(';'):
        if '=' in item:
            key, value = item.split('=', 1)
            attrs[key] = value
    return attrs

def parse_gff_line(line):
    """Parse a GFF line with extracted feature names and IDs"""
    if line.startswith('#'):
        return None
    
    fields = line.strip().split('\t')
    if len(fields) < 9:
        return None
    
    # Parse attributes
    attrs = parse_attributes(fields[8])
    
    # Extract gene name and ID
    gene_name = attrs.get('Name', '')
    gene_id = attrs.get('Dbxref', '').split(',')[0] if 'Dbxref' in attrs else ''
    
    return {
        'chr': fields[0],
        'start': fields[3],
        'end': fields[4],
        'feature_type': fields[2],
        'feature_source': fields[1],
        'feature_strand': fields[6],
        'feature_score': fields[5],
        'feature_phase': fields[7],
        'feature_name': gene_name,
        'feature_id': gene_id,
        'full_attributes': fields[8]
    }

def convert_to_bed(df, output_file):
    """Convert annotation dataframe to BED format"""
    bed_df = df[['CHR', 'START', 'END']]
    bed_df.to_csv(output_file, sep='\t', header=False, index=False)

def main():
    parser = ArgumentParser(description='Find genomic features in regions using bedtools')
    parser.add_argument('--anno', required=True, help='Input annotation file (CHR, START, END)')
    parser.add_argument('--gff', required=True, help='Reference GFF file')
    parser.add_argument('--output', required=True, help='Output file name')
    
    args = parser.parse_args()
    
    # Read regions file
    print("Reading regions file...")
    regions = pd.read_csv(args.anno, sep='\t')
    
    # Convert regions to BED format
    convert_to_bed(regions, "regions.bed")
    
    # Run bedtools intersect
    print("\nRunning bedtools intersect...")
    cmd = f"bedtools intersect -a {args.gff} -b regions.bed -wa"
    
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        intersections = result.stdout.strip().split('\n')
        
        results = []
        for line in intersections:
            if line:
                gff_fields = parse_gff_line(line)
                if gff_fields:
                    results.append(gff_fields)
        
        # Create output dataframe
        results_df = pd.DataFrame(results)
        if not results_df.empty:
            # Reorder columns to put feature_name and feature_id more prominently
            cols = ['chr', 'start', 'end', 'feature_type', 'feature_name', 'feature_id', 
                   'feature_source', 'feature_strand', 'feature_score', 'feature_phase', 
                   'full_attributes']
            results_df = results_df[cols]
            
            results_df.to_csv(args.output, sep='\t', index=False)
            print(f"\nResults written to {args.output}")
            print(f"Found {len(results_df)} intersecting features")
        else:
            print("\nNo intersecting features found")
            
    except subprocess.CalledProcessError as e:
        print(f"Error running bedtools: {e}")
        
    # Cleanup
    subprocess.run("rm regions.bed", shell=True)

if __name__ == "__main__":
    main()
