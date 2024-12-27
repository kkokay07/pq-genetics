---

# README: Genome Annotation Pipeline

## Overview
This pipeline annotates genomic regions of interest using a `.gff` file downloaded from the NCBI Genome Database. It outputs feature annotations and a bar plot showing the distribution of features.

---

## Pre-Steps

### Pre-Step 1: Download the `.gff` File from NCBI
1. **Go to NCBI Genome Database**:
   - Open [NCBI Genome Database](https://www.ncbi.nlm.nih.gov/genome/).

2. **Search for Your Organism or Genome**:
   - Use the search bar to find your genome of interest (e.g., *Bos taurus*, *Escherichia coli*).

3. **Locate the Genome Assembly**:
   - From the search results, click on the genome assembly name.

4. **Find and Download the `.gff` File**:
   - Scroll to the **"Assembly and Annotation"** or **"Download Assemblies"** section.
   - Download the `.gff` or `.gff3` file.

5. **Prepare the `.gff` File**:
   - Unzip the downloaded file.
   - Place it in your working directory.

---

### Pre-Step 2: Install Required Python Libraries

Run the following command to install the necessary Python libraries:

```bash
pip install pandas matplotlib seaborn tqdm
```

---

## Step-by-Step Instructions

### Step 1: Prepare the `input.txt` File
1. Create a **tab-separated** file named `input.txt` with the following structure:
   - Columns: `CHR`, `START`, `END`.
   - Ensure chromosome IDs match the reference assembly from NCBI.

#### Example `input.txt`:
```
CHR	START	END
NC_059179.1   34133847   34183847
NC_059180.1   4133847   41838470
```

> **Tip**: To find the correct chromosome IDs:
> - Search for your genome assembly on NCBI.
> - Scroll to the table containing chromosome numbers and IDs.

---

### Step 2: Annotate Genomic Regions
Run the following code to generate a TSV file with annotated features:

```bash
python3 1.snp2feature.py --anno input.txt --gff genomic.gff --output result.tsv
```

- **Input**: `input.txt` (tab-separated file with CHR, START, END columns).
- **GFF File**: `genomic.gff` (downloaded in Pre-Step 1).
- **Output**: `result.tsv` (feature annotations).

---

### Step 3: Visualize Feature Distribution
Generate a bar plot of feature distribution using the following code:

```bash
python3 2.feature2visual.py --input result.tsv --output feature_distribution.png
```

- **Input**: `result.tsv` (output from Step 2).
- **Output**: `feature_distribution.png` (bar plot of feature distribution).

---

## Expected Outputs

1. **Annotation File (`result.tsv`)**: Tabular file containing genomic features such as `exon`, `CDS`, `gene`, `lnc_RNA`, `mRNA`, `tRNA`, etc.
2. **Visualization (`feature_distribution.png`)**: Bar plot showing the distribution of features.

---

## Notes
- Ensure all paths and filenames match your working directory setup.
- Verify Python version (`Python 3.x`) and library compatibility.

---
### It's a peanut!
