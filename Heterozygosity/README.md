# Heterozygosity Analysis and Visualization

## Overview

The pipeline consists of two main steps:
1. Calculating heterozygosity statistics (Ho, He, and F) using PLINK
2. Visualizing the results using a custom Python script


## Usage

### Step 1: Calculate Heterozygosity Statistics

Use PLINK to calculate observed heterozygosity (Ho), expected heterozygosity (He), and inbreeding coefficient (F):

```bash
plink --bfile data_plink --het --out results
```

This command:
- Takes binary PLINK files as input (data_plink.bed, data_plink.bim, data_plink.fam)
- Calculates heterozygosity statistics
- Outputs results to results.het

The output file (results.het) contains the following columns:
- FID: Family ID
- IID: Individual ID
- O(HOM): Observed number of homozygotes
- E(HOM): Expected number of homozygotes
- N(NM): Number of non-missing genotypes
- F: Inbreeding coefficient F

### Step 2: Visualize Results

Use the provided Python script to create a visualization:

```bash
python3 plink_het2visual.py plink.het results.het --title "Heterozygosity Distribution"
```

Parameters:
- First argument: Input .het file from PLINK
- Second argument: Output filename
- --title: Optional plot title

## Notes

- Negative F values if present, that individuals will be removed only for this metrics while calcualting the average.


## 👨‍🔬 About the Author

**Dr. Kanaka K. K., PhD, ARS**  
Scientist  
School of Bioinformatics  
[ICAR-Indian Institute of Agricultural Biotechnology, Ranchi](https://iiab.icar.gov.in/)
> [Be like IIAB!:](https://www.researchgate.net/publication/379512649_ICAR-IIAB_Annual_Report-_2023) IIAB is like yogic center where all the sciences (Plant, Animal, Aquatic,Mibrobiology, IT) meet to address emerging issues in food production.

## 🔎 Spy on me
- [Google Scholar](https://scholar.google.com/citations?hl=en&user=0dQ7Sf8AAAAJ&view_op=list_works&sortby=pubdate)
- [GitHub: kkokay07](https://github.com/kkokay07)
- [ResearchGate](https://www.researchgate.net/profile/Kanaka-K-K/research)
- [Institute Website](https://iiab.icar.gov.in/staff/dr-kanaka-k-k/)

