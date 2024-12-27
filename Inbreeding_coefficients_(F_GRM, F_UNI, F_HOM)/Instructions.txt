```markdown
# README.md

## IBC Visualization Pipeline

This repository provides a streamlined workflow for generating and visualizing Inbreeding Coefficients (IBC) using PLINK and Python. 

---

### Prerequisites

Before starting, ensure that you have the required tools and libraries installed on your system. Follow the steps below for installation and execution.

---

### Pre-step 1 (Optional): Install PLINK

If PLINK is not installed on your system, follow these instructions:

1. Visit the official [PLINK website](https://www.cog-genomics.org/plink/).
2. Download the **Stable (beta 7.7)** version (available as of Dec 25, 2024).
3. Extract the downloaded file:
   ```bash
   unzip plink_bla_bla_bla.zip
   ```
   *Note: Replace `bla_bla_bla` with the specific name of the downloaded file.*
4. Optionally, add PLINK to your PATH for convenient access from any directory:
   ```bash
   export PATH=$PATH:/path/to/plink
   ```
   Replace `/path/to/plink` with the location of the extracted PLINK binary.

---

### Step 1: Generate IBC Output

Run the following command in your terminal to calculate the inbreeding coefficients and generate the output file (`output.ibc`):

```bash
plink --bfile input_file --ibc --out output
```

Replace `input_file` with the base name of your input files (e.g., `.bed`, `.bim`, and `.fam`).

---

### Pre-step 2 (Optional): Install Python Libraries

Install the necessary Python libraries by running:

```bash
pip install pandas matplotlib seaborn numpy
```

---

### Step 2: Visualize IBC Data

Run the following Python script to visualize the IBC data. The script will prompt you to specify the input file (e.g., `output.ibc` generated in Step 1) and save the visualization as `output.png` (600 dpi).

```bash
python3 ibc2visual.py
```

---

### Output

- **`output.ibc`**: File containing IBC results (generated in Step 1).
- **`output.png`**: Visualization of the IBC results (generated in Step 2).

---

### It's a peanut!
