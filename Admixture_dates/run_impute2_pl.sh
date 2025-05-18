#!/bin/bash
for ((chromosome=1; chromosome<=24; chromosome++))
do
    perl impute2chromopainter2.pl -p "chr${chromosome}_phased.haps" "map${chromosome}.txt" "chr${chromosome}"
done
