# PlinkPhylo (PLINK to Phylogeny)

This utility converts Identity-By-State (IBS) distance matrices produced by "PLINK" from binary genotype files into "ape" R-package compatible format for phylogenetic analysis.

## Requirements

- [PLINK 1.9+](https://www.cog-genomics.org/plink/)
- R 4.4.x

## Step 1: Generate `.mibs` and `.mibs.id` Files Using PLINK

Ensure you have your PLINK binary files (`.bed`, `.bim`, `.fam`) ready. Use the following command to compute the IBS distance matrix:

```bash
plink \
  --bfile input \
  --allow-extra-chr \
  --distance ibs flat-missing square \
  --out out_ibsdist
```
Explanation of PLINK options:

    --bfile: Prefix of your PLINK binary files (.bed, .bim, .fam).

    --allow-extra-chr: Allows non-standard chromosome names.

    --distance ibs flat-missing square: Computes the pairwise IBS distance matrix, outputs in square lower triangle format with flat-missing encoding.

    --out: Output prefix, will generate:

        out_plink_ibsdist.mibs: IBS distance matrix

        out_plink_ibsdist.mibs.id: Corresponding sample IDs

## Step 2: Construct Neighbor-Joining Tree in "ape" R-package

Use the following R script to construct a Neighbor-Joining (NJ) tree from the `.mibs` and `.mibs.id` files and save it in MEGA-compatible Newick format:

```r
# Load required package
if (!require("ape")) install.packages("ape", dependencies = TRUE)
library(ape)

# Read .mibs.id and .mibs files
ids <- read.table("out_plink_ibsdist.mibs.id")
dist_matrix <- as.matrix(read.table("out_plink_ibsdist.mibs"))

# Set row and column names
rownames(dist_matrix) <- ids$V1
colnames(dist_matrix) <- ids$V1

# Convert to distance object
dist_object <- as.dist(dist_matrix)

# Construct NJ tree
nj_tree <- nj(dist_object)

# Save as Newick format (lightweight, MEGA-compatible)
write.tree(nj_tree, file = "phylo_nj_tree.newick")

# Plot tree
plot(nj_tree, cex = 0.6)
title("Neighbor-Joining Tree")
