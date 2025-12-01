#!/bin/bash

# Loop from 1 to 29
for i in {1..29}; do
  echo "Running prefileforlamp.sh for chromosome $i"
  sh prefileforlamp.sh "$i" allLoCaBreed_TOP_QC
done
