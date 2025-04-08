# PlinkPhylo (PLINK to Phylogeny)

A Python tool for creating population-based phylogenetic trees from individual-based distance matrices. This piplene converts Identity-By-State (IBS) distance matrices produced by "PLINK" from binary genotype files, later Plink2Phylo.py will convert IBS matrices to infer phylogeny.

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

## Step 2: Construct Neighbor-Joining Tree 

## Installation

Install the required packages:

```bash
pip install -r requirements.txt
```

## Usage

```bash
python Plink2Phylo.py -d out_plink_ibsdist.mibs -i out_plink_ibsdist.mibs.id -o output
```

### Required Arguments

- `-d, --dist` : Path to the distance matrix file (.mibs)
- `-i, --ids` : Path to the IDs file (.mibs.id)

### Optional Arguments

- `-p, --pop` : Path to the population assignment file
- `-o, --output` : Output prefix for generated files (default: "population_tree")
- `-m, --method` : Method to extract populations:
  - 'auto' (from ID prefix)
  - 'file' (from file)
  - 'custom:X' (custom pattern)
- `--pattern` : Regex pattern to extract populations when using auto method (default: "^[A-Z]+")
- `--min-samples` : Minimum samples required per population to include in analysis (default: 1)
- `--no-plots` : Skip creating plot files

## Output Files

The script generates the following output files:

- `[prefix]_individual.newick` : Individual-based tree in Newick format
- `[prefix]_population.newick` : Population-based tree in Newick format
- `[prefix]_individual.txt` : Text representation of the individual tree
- `[prefix]_population.txt` : Text representation of the population tree
- `[prefix]_individual_colored.txt` : Text file with population information and tree structure

## Troubleshooting

If you encounter Qt-related errors when generating plots, you have several options:

1. Install the Qt dependencies as shown in the installation section
2. Use the `--no-plots` option to skip plot generation
3. The current version outputs text files instead of PDFs to avoid Qt dependencies
4. To visualize the Newick files, you can use external tools like:
   - FigTree (https://github.com/rambaut/figtree/)
   - iTOL (https://itol.embl.de/)
   - ETE3 Toolkit's webserver (http://etetoolkit.org/treeview/)

## Notes

- The script uses a simplified neighbor-joining approximation
- Population assignments are extracted from IDs using regex patterns by default
- For larger datasets, the process may take some time, especially during the population distance calculation step
plot(nj_tree, cex = 0.6)
title("Neighbor-Joining Tree")
