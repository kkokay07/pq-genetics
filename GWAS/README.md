# GWAS Analysis Pipeline Using GCTA

A comprehensive pipeline for conducting Genome-Wide Association Studies (GWAS) using GCTA software, from data preparation to result visualization.

## Table of Contents
- [Installation](#installation)
- [Pipeline Overview](#pipeline-overview)
- [Data Preparation](#data-preparation)
  - [Phenotype Processing](#phenotype-processing)
  - [Covariate Preparation](#covariate-preparation)
- [Analysis Steps](#analysis-steps)
- [Visualization](#visualization)
- [Annotation](#annotation)

## Installation

1. Download and install GCTA from the [official website](https://yanglab.westlake.edu.cn/software/gcta/#Download)
2. Install required Python libraries:
   ```bash
   pip install numpy pandas matplotlib seaborn scipy statsmodels
   ```

## Pipeline Overview

1. Phenotype distribution analysis
2. Data normalization
3. Sample selection
4. Covariate analysis
5. GRM creation
6. Population structure analysis
7. GWAS execution
8. Result visualization
9. Variant annotation

## Data Preparation

### Phenotype Processing

1. **Check Trait Distribution**
   ```bash
   python pheno_distribution.py phenotype.txt --out my_analysis
   ```

   Required format for `phenotype.txt`:
   | FID  | IID  | Trait1 | Trait2 |
   |------|------|--------|--------|
   | 1    | 1    | 23.5   | -9     |
   | 2    | 2    | 45.2   | 32.1   |

2. **Normalize Non-Normal Traits**
   ```bash
   python pheno_normalizer.py input.txt --out normalized_output.txt
   ```

### Covariate Preparation

1. **Create Covariates File**
   
   Format for `covariates.txt`:
   | FID  | IID  | F1 | F2 | F3 | F4 | F5 |
   |------|------|----|----|----|----|----|
   | 1    | 1    | 1  | 5  | 5  | 11 | 175|

2. **Select Important Factors**
   ```bash
   python3 fixed_factor_checker.py
   ```

   Selection criteria:
   - R² > 0.05
   - Correlation < 0.7
   - VIF < 10

## Analysis Steps

### 1. Create Genetic Relationship Matrix (GRM)
```bash
gcta64 --bfile your_data --make-grm --out myGRM --thread-num 10
```

### 2. Subset GRM
```bash
gcta64 --grm myGRM \
    --keep ind.txt \
    --make-grm \
    --out pop1_grm_subset
```
   Format for `ind.txt`:
   | FID  | IID  |
   |------|------|
   | 1    | 1    |
   | 1    | 2    |
   | .    | .    |
   
### 3. Principal Component Analysis
```bash
gcta64 --grm your_grm \
    --pca 20 \
    --out your_pca
```

Evaluate PCs:
```bash
python pc_decider.py your_pca.eigenval
```

### 4. GWAS Execution
```bash
gcta64 --mlma --bfile mehsana \
    --grm sp_grm_subset \
    --pheno trait.txt \
    --qcovar mehsana_pca_10.eigenvec \
    --covar covar.txt \
    --out trait_gwas --thread-num 4
```
> If no covariates are there, simply remove --covar covar.txt \

## Visualization

1. **Generate Manhattan Plot**
   ```bash
   python3 gwas_analyser.py my_gwas.mlma --out my --snps 53913
   ```

2. **Estimate Top SNP Variation**
   ```bash
   python3 var_by_1percent_snp.py
   ```

## Annotation

For annotating significant variants:

1. Visit the [Annotation Repository](https://github.com/kkokay07/pq-genetics/tree/main/Annotation_of_features)
2. Follow repository instructions for feature annotation

## Notes

- Ensure consistent sample IDs across all files
- Back up data before normalization
- Monitor memory usage during GRM creation
- Consider parallelization for large datasets

---

🥜 It's a peanut!
