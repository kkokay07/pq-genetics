#!/bin/bash

# Loop through chromosomes 1 to 24
for chr in {1..24}; do
    echo "Processing chromosome $chr"
    ./ChromoPainterv2 -g chr${chr}.haps -r chr${chr}.recomrates -t ind_MSM.txt -f popsur_MSM.txt 1 10 -s 0 -i 10 -in -iM -o output_estimateEM_Chr${chr}
done

