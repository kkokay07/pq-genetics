# Genome Annotation Pipeline

A Python-based pipeline for annotating genomic regions of interest using NCBI Genome Database GFF files. The pipeline provides feature annotations and visualization of feature distributions.

## Table of Contents
- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Data Preparation](#data-preparation)
- [Usage](#usage)
- [Outputs](#outputs)
- [Notes](#notes)

## Overview

This pipeline processes genomic regions of interest using GFF annotation files from NCBI. It generates:
- Feature annotations in TSV format
- Visualization of feature distribution as a bar plot

## Prerequisites

- Python 3.x
- Internet connection (for downloading GFF files)
- Access to NCBI Genome Database

## Installation

Install required Python libraries:

```bash
pip install pandas matplotlib seaborn tqdm
```

## Data Preparation

### 1. Download GFF File from NCBI

1. Visit the [NCBI Genome Database](https://www.ncbi.nlm.nih.gov/genome/)
2. Search for your organism (e.g., *Bos taurus*, *Escherichia coli*)
3. Navigate to the genome assembly page
4. Download the GFF/GFF3 file from the "Assembly and Annotation" section
5. Extract the downloaded file to your working directory

### 2. Prepare Input File

Create a tab-separated file named `input.txt` with the following columns:
- CHR (Chromosome ID)
- START (Start position)
- END (End position)

Example `input.txt`:
```
CHR	START	END
NC_059179.1   34133847   34183847
NC_059180.1   4133847   41838470
```

> **💡 Tip**: Find correct chromosome IDs in the NCBI genome assembly information table.

## Usage

### 1. Feature Annotation

Generate feature annotations:

```bash
python 1.snp2feature.py --anno imput.txt --gff reference.gff --output result.tsv
```

Parameters:
- `--anno`: Input file with genomic regions
- `--gff`: GFF file from NCBI
- `--output`: Output TSV file name

### 2. Visualization

Create feature distribution plot:

```bash
python3 2.feature2visual.py --input input.txt --gff reference.gff --output result --trait "trait name" --dpi 600
```

## Outputs

1. **Feature Annotations** (`result.tsv`)
   - Tab-separated file containing genomic features
   - Includes features like: exon, CDS, gene, lnc_RNA, mRNA, tRNA

2. **Feature Distribution** 
   - Bar plot and Pie chart plot visualization
   - Shows distribution of different feature types

## Notes

- Ensure chromosome IDs in your input file match the reference assembly
- Verify file paths and permissions in your working directory
- Check Python version compatibility before running
- Keep GFF and input files in the same directory as scripts

---

🥜 It's a peanut!
