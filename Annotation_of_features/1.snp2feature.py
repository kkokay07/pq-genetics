import pandas as pd
from argparse import ArgumentParser
from tqdm import tqdm

def read_regions(anno_file):
    """Read the annotation file containing regions of interest"""
    return pd.read_csv(anno_file, sep='\t')

def parse_gff_feature(line):
    """Parse a GFF line to extract all features"""
    if line.startswith('#'):
        return None
    
    fields = line.strip().split('\t')
    if len(fields) < 9:
        return None
        
    chrom = fields[0]
    feature_source = fields[1]
    feature_type = fields[2]
    start = int(fields[3])
    end = int(fields[4])
    score = fields[5]
    strand = fields[6]
    phase = fields[7]
    
    # Parse attributes
    attrs = {}
    if fields[8] != '.':
        for item in fields[8].split(';'):
            if '=' in item:
                key, value = item.split('=', 1)
                attrs[key] = value
    
    return {
        'chr': chrom,
        'source': feature_source,
        'type': feature_type,
        'start': start,
        'end': end,
        'score': score,
        'strand': strand,
        'phase': phase,
        'id': attrs.get('ID', 'Unknown'),
        'name': attrs.get('Name', attrs.get('ID', 'Unknown')),
        'attributes': fields[8]
    }

def check_overlap(region, feature):
    """Check if a feature overlaps with a region"""
    return (region['CHR'] == feature['chr'] and 
            region['START'] <= feature['end'] and 
            region['END'] >= feature['start'])

def main():
    parser = ArgumentParser(description='Find genomic features in regions')
    parser.add_argument('--anno', required=True, help='Input annotation file (CHR, START, END)')
    parser.add_argument('--gff', required=True, help='Reference GFF file')
    parser.add_argument('--output', required=True, help='Output file name')
    
    args = parser.parse_args()
    
    # Read regions file
    print("Reading regions file...")
    regions = read_regions(args.anno)
    print("\nInput regions:")
    print(regions)
    
    # Process GFF file and find overlaps
    print("\nFinding overlapping features...")
    results = []
    
    # Main processing
    total_lines = sum(1 for _ in open(args.gff))
    processed_features = 0
    
    with open(args.gff) as f:
        for line in tqdm(f, total=total_lines, desc="Processing GFF file"):
            feature = parse_gff_feature(line)
            if feature is None:
                continue
                
            processed_features += 1
            # Check each region for overlap
            for _, region in regions.iterrows():
                if check_overlap(region, feature):
                    results.append({
                        'region_chr': region['CHR'],
                        'region_start': region['START'],
                        'region_end': region['END'],
                        'feature_type': feature['type'],
                        'feature_source': feature['source'],
                        'feature_id': feature['id'],
                        'feature_name': feature['name'],
                        'feature_start': feature['start'],
                        'feature_end': feature['end'],
                        'feature_strand': feature['strand'],
                        'feature_score': feature['score'],
                        'feature_phase': feature['phase'],
                        'feature_attributes': feature['attributes']
                    })
    
    print(f"\nProcessed {processed_features} features from GFF file")
    
    # Create output dataframe and save
    results_df = pd.DataFrame(results)
    if not results_df.empty:
        # Sort by feature type and position
        results_df = results_df.sort_values(['region_chr', 'feature_type', 'feature_start'])
        
        # Save to CSV
        results_df.to_csv(args.output, index=False, sep='\t')
        
        # Print summary
        print(f"\nResults written to {args.output}")
        print(f"Found {len(results_df)} feature overlaps across {len(regions)} regions")
        
        # Show feature type breakdown
        print("\nFeature type breakdown:")
        type_counts = results_df['feature_type'].value_counts()
        for feat_type, count in type_counts.items():
            print(f"{feat_type}: {count}")
    else:
        print("\nNo overlapping features found in the specified regions")

if __name__ == "__main__":
    main()
