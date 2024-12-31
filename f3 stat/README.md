# f3 stats using treeMix 

## Prerequisites
- PLINK v1.9
- Python 3
- TreeMix
- threepop

## Installation

### TreeMix Installation
```bash
# Install dependencies
sudo apt-get install git automake g++ libtool pkg-config

# Clone TreeMix repository
git clone https://github.com/davidemms/treemix.git
cd treemix

# Build and install
./autogen.sh
./configure
make
sudo make install
```

## Analysis Pipeline

### Step 1: Generate Frequency Files
Generate allele frequency files for each population:
```bash
plink --bfile pop6 --freq --family --out x
```
Output: x.frq.strat

### Step 2: Convert to TreeMix Format
Convert PLINK frequency files to TreeMix input format:
```bash
python3 plink2treemix.py --freq x.frq.strat --out x.treemix.gz
```
Output: x.treemix.gz

### Step 3: Run Three-Population Test
Perform f3 statistics calculation:
```bash
threepop -i x.treemix.gz -k 1000 > f3_results.txt
```
Output: f3_results.txt

### Step 4: Visualize Results
Generate visualization of the results:
```bash
python3 threepop2visual.py
```

## Input Files
- PLINK binary files (.bed, .bim, .fam)
- Population identifiers in PLINK family file

## Output Files
- f3_results.txt: Three-population test results

## Citations
- Pickrell J, Pritchard J (2012). TreeMix: Inference of Population Tree and Admixture Events.
- Patterson N, et al. (2012). Ancient Admixture in Human History.

## Author
**Dr. Kanaka K. K., PhD, ARS**  
Scientist  
School of Bioinformatics  
ICAR-Indian Institute of Agricultural Biotechnology, Ranchi
