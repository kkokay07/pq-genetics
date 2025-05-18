#!/bin/bash
# Loop through chromosomes 1-24
for chr in {1..24}
do
    input_file="chr${chr}_phased.haps"
    map_file="map${chr}.txt"
    output_prefix="chr${chr}"
    
    # Check if both input and map files exist before processing
    if [ -f "$input_file" ] && [ -f "$map_file" ]; then
        echo "Processing chromosome ${chr}..."
        perl impute2chromopainter2.pl -p "$input_file" "$map_file" "$output_prefix"
    else
        echo "Warning: Input file ${input_file} or map file ${map_file} not found, skipping..."
    fi
done
