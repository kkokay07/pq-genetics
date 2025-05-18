#!/bin/bash

for chr in {25..26}; do
    /home/hp/Documents/Admixture_date/Chromopainter/All_sample_run_copy/ChromoPainterv2 -g "cdtcp${chr}.haps" -r "cdtcp${chr}.recomrates" -t INDI.txt -f POPSURR_step8.txt 0 0 -s 10 -n 3171.687 -M 0.003814 -o "chr${chr}_DonorvTarget"
done

