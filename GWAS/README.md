## **GWAS Analysis Using GCTA**

**Link to download and install GCTA:** https://yanglab.westlake.edu.cn/software/gcta/#Download

### **Step 1: Check the Distribution of a Trait**
Quantitative traits should typically follow a normal distribution. Use the following command to visualize the distribution:

```bash
python pheno_distribution.py phenotype.txt --out my_analysis
```

**Format of phenotype.txt:**

| FID  | IID  | Trait1 | Trait2 |
|------|------|--------|--------|
| 1    | 1    | 23.5   | -9     |
| 2    | 2    | 45.2   | 32.1   |
| 3    | 3    | -9     | 28.4   |
| 4    | 4    | 28.7   | 35.2   |

### **Step 2: Normalize Non-Normal Traits**
If some traits do not follow a normal distribution, normalize them using the following command:

```bash
python pheno_normalizer.py input.txt --out normalized_output.txt
```

**Format of input.txt:**

| FID  | IID  | Phenotype |
|------|------|-----------|
| 1    | 1    | 23.5      |
| 2    | 2    | 45.2      |
| 3    | 3    | 32.1      |
| 4    | 4    | 28.7      |

### **Step 3: Select Subset of Individuals**
To select a subset of individuals when traits and fixed factors are present in separate files, use the following command:

```bash
awk 'NR==FNR {a[$1]=$2; next} $1 in a {print $0, a[$1]}' gt.txt pt.txt > SP_vlookup.txt
```

Copy the output into an Excel sheet, then prepare a `phenotype.txt` file with the following format:

| FID           | IID           | Trait |
|---------------|---------------|-------|
| 340021495092  | 340021495092  | 411   |
| 340099458491  | 340099458491  | 238   |
| 340099452002  | 340099452002  | 104   |
| 340014504815  | 340014504815  | 147   |

### **Step 4: Prepare Covariates**
Create a `covariates.txt` file containing all covariates:

| FID           | IID           | F1 | F2 | F3 | F4 | F5 |
|---------------|---------------|----|----|----|----|----|
| 340021495092  | 340021495092  | 1  | 5  | 5  | 11 | 175 |
| 340099458491  | 340099458491  | 1  | 3  | 7  | 9  | 73  |
| 340099452002  | 340099452002  | 1  | 3  | 7  | 9  | 142 |
| 340014504815  | 340014504815  | 1  | 3  | 8  | 10 | 140 |

### **Step 5: Identify Relevant Fixed Factors**
Run the following script to identify important fixed factors for a specific trait:

```bash
python3 fixed_factor_checker.py
```

This will open a popup menu where you can select the phenotype and covariate files.

**Guidelines for Factor Selection:**
1. Include factors with R² > 0.05.
2. Remove or combine highly correlated factors (correlation > 0.7).
3. Remove factors with VIF > 10 to avoid multicollinearity issues.

Prepare a new covariate file with only the important factors.

### **Step 6: Create the GRM**
Use all individuals in the PLINK binary file to create a genetic relationship matrix (GRM):

```bash
gcta64 --bfile your_data --make-grm --out myGRM --thread-num 10
```

### **Step 7: Subset the GRM to Phenotyped Individuals**

```bash
gcta64 --grm myGRM \
    --keep ind.txt \
    --make-grm \
    --out pop1_grm_subset
```

### **Step 8: Perform PCA**
Create principal components (PCs) from the GRM:

```bash
gcta64 --grm your_grm \
    --pca 20 \         # Calculate first 20 PCs
    --out your_pca
```

Evaluate which PCs to retain:

```bash
python pc_analyzer.py your_pca.eigenval
```

Select only the important PCs:

```bash
cut -f1-$((N+2)) your_pca.eigenvec > your_pca_significant.eigenvec
```

### **Step 9: Run GWAS**
Run the GWAS, adjusting for fixed factors, genetic relationships, and population structure:

```bash
gcta64 --mlma --bfile mehsana \
    --grm sp_grm_subset \
    --pheno SP_vlookup.txt \
    --qcovar mehsana_pca_10.eigenvec \
    --covar sp_covar.txt \
    --out sp_gwas --thread-num 4
```

### **Step 10: Visualize Results**
Generate a Manhattan plot and find significant associations:

```bash
python3 gwas_analyser.py my_gwas.mlma --out my --snps 53913
```

### **Step 11: Estimate Variation Explained by Top 1% SNPs**

```bash
python3 var_by_1percent_snp.py
```

This script will detect all `.mlma` files in the folder and prompt for trait names.

### **Step 12: Annotation**
Use the following GitHub repository for annotation:

[Annotation of Features](https://github.com/kkokay07/pq-genetics/tree/main/Annotation_of_features)

Follow the instructions provided in the repository.

---
Thats all!
