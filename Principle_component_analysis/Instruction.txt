# Principal Component Analysis (PCA) Pipeline

A streamlined workflow for performing and visualizing Principal Component Analysis using PLINK and Python.

## Table of Contents
- [Installation](#installation)
  - [PLINK Setup](#plink-setup)
  - [Python Dependencies](#python-dependencies)
- [Usage](#usage)
  - [Generate PCA](#generate-pca)
  - [Visualize Results](#visualize-results)
- [Output Files](#output-files)
- [Additional Notes](#additional-notes)

## Installation

### PLINK Setup

1. Download PLINK:
   - Visit the [PLINK website](https://www.cog-genomics.org/plink/)
   - Download Stable (beta 7.7) version

2. Extract the downloaded file:
   ```bash
   unzip plink_bla_bla_bla.zip
   ```
   Note: Replace `plink_bla_bla_bla` with your downloaded file name

3. Add PLINK to PATH (optional but recommended):
   ```bash
   export PATH=$PATH:/path/to/plink
   ```
   Replace `/path/to/plink` with your PLINK binary location

### Python Dependencies

Install required Python libraries:
```bash
pip install pandas matplotlib numpy scipy
```

## Usage

### Generate PCA

Run PLINK to perform PCA analysis:
```bash
plink --cow --bfile input_file --pca --out result
```

Note: Replace `--cow` with appropriate species flag if not working with cattle data. Check PLINK documentation for other species options.

### Visualize Results

Create PCA visualization with population ellipses:
```bash
python3 pca_visualization.py \
    --eigenvec result.eigenvec \
    --eigenval result.eigenval \
    --fam input_file.fam \
    --ellipse-pops pop1 pop2 \
    --dpi 600
```

Parameters:
- `--eigenvec`: PLINK eigenvalues file
- `--eigenval`: PLINK eigenvectors file
- `--fam`: PLINK family file
- `--ellipse-pops`: Space-separated list of populations for ellipse drawing
- `--dpi`: Output image resolution (default: 600)

## Output Files

1. PLINK PCA Output:
   - `result.eigenvec`: Contains principal components
   - `result.eigenval`: Contains eigenvalues

2. Visualization:
   - High-resolution PCA plot (600 DPI)
   - Population-specific ellipses
   - Variance explained by each component

## Additional Notes

- Ensure input files are in PLINK binary format (`.bed`, `.bim`, `.fam`)
- You can specify any number of populations in `--ellipse-pops`
- Higher DPI values will produce larger file sizes
- Check PLINK documentation for species-specific flags

---

🥜 It's a peanut!
