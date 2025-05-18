#!/bin/bash

# Loop through chromosomes 1 to 24
for chr in {25..26}; do
    echo "Processing chromosome ${chr}..."
    
    /home/hp/Documents/Admixture_date/Chromopainter/All_sample_run_copy/ChromoPainterv2 -g "cdtcp${chr}.haps" \
                      -r "cdtcp${chr}.recomrates" \
                      -t INDI.txt \
                      -f POPSURR.txt \
                      0 0 \
                      -s 0 \
                      -n 3171.687 \
                      -M 0.003814 \
                      -o "cdtcp${chr}_DonorvALL"
                      
    echo "Finished chromosome ${chr}"
done

echo "All chromosomes completed"
