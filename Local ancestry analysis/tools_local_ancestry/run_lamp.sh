#!/bin/bash

# Loop from 1 to 29
for i in {1..29}; do
  echo "Running ./lamp command for chromosome $i"
  ./lamp "allLoCaBreed_TOP_QC_CHR${i}configfile.txt"
done
