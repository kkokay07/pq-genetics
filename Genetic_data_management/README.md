# PLINK Commands for Genetic Data Management

A comprehensive reference guide for common PLINK operations in genetic data analysis.

## Table of Contents
- [File Format Conversions](#file-format-conversions)
- [Sample Management](#sample-management)
- [Data Merging](#data-merging)
- [Quality Control](#quality-control)
- [Data Analysis](#data-analysis)
- [Advanced Operations](#advanced-operations)

## File Format Conversions

### 1. Binary to MAP/PED
```bash
./plink --noweb --bfile input --cow --nonfounders \
    --allow-no-sex --recode --out output
```

### 2. MAP/PED to Binary
```bash
./plink --file input --cow --make-bed --out output
```

### 3. MAP/PED to VCF
```bash
./plink --cow --file input --recode vcf-iid --out output
```

### 4. VCF to MAP/PED
```bash
vcftools --vcf input.vcf --plink --out output
```

### 5. VCF to Binary
```bash
./plink --cow --allow-extra-chr --vcf input.vcf --make-bed --out output
```

## Sample Management

### 6. Rename Samples
```bash
./plink --cow --bfile input --fam rename.fam --make-bed --out output
```

### 7. Extract SNPs
```bash
./plink --noweb --file input --cow --extract mysnps.txt \
    --allow-no-sex --make-bed --out output
```
*mysnps.txt format:*
```
rs12345
rs67890
rs112233
```

### 8. Extract Individuals
```bash
./plink --noweb --file input --cow --keep mylist.txt --make-bed --out output
```
*mylist.txt format:*
```
F1    IID1
F2    IID2
F3    IID3
```

## Data Merging

### 9. Merge Two Files
```bash
# Using PED/MAP
./plink --cow --file data1 --merge data2.ped data2.map --make-bed --out output

# Using Binary
./plink --cow --bfile data1 --bmerge data2.bed data2.bim data2.fam \
    --make-bed --out output
```

### 10. Merge Multiple Files
```bash
./plink --cow --file file1 --merge-list merge_list.txt --make-bed --out output
```
*merge_list.txt format:*
```
file2.ped file2.map
file3.ped file3.map
file4.bed file4.bim file4.fam
```

## Quality Control

### 11. Filter by MAF
```bash
./plink --bfile input --maf 0.05 --make-bed --out output_maf05
```

### 12. Filter by Genotype Missing Rate
```bash
# Remove SNPs with >10% missing data
./plink --bfile input --geno 0.1 --make-bed --out output_geno

# Remove individuals with >10% missing data
./plink --bfile input --mind 0.1 --make-bed --out output_mind
```

### 13. Hardy-Weinberg Equilibrium Test
```bash
./plink --bfile input --hwe 1e-6 --make-bed --out output_hwe
```

### 14. LD Pruning
```bash
./plink --bfile input \
    --indep-pairwise 50 5 0.2 \
    --out pruned
    
./plink --bfile input \
    --extract pruned.prune.in \
    --make-bed --out output_pruned
```

## Data Analysis

### 15. Calculate Allele Frequencies
```bash
./plink --bfile input --freq --out allele_freqs
```

### 16. Check Sex Discrepancies
```bash
./plink --bfile input --check-sex --out sex_check
```

### 17. Calculate Missing Rates
```bash
# By individual
./plink --bfile input --missing --out missing_stats

# By SNP
./plink --bfile input --lmiss --out snp_missing
```


## Tips & Notes

1. Always backup data before running commands
2. Use `--allow-no-sex` when sex information is missing
3. Add `--cow` flag for cattle data analysis only. For other species check in plink website
4. Use `--noweb` to prevent web check (older PLINK versions)
5. Monitor disk space when working with large datasets
6. Consider using `--thread-num` for parallel processing

---

🥜 It's a peanut!
