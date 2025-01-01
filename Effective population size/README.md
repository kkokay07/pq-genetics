# GONE Installation and Ne Estimation Guide

## GONE (Genomic Estimates of Ne)

GONE calculates effective population size (Ne) trajectories over ~100-200 generations using linkage disequilibrium from genomic markers.

## Installation

```bash
# Clone repository
git clone https://github.com/esrud/GONE.git

# Navigate to Linux directory
cd GONE/Linux

# Make executables runnable 
chmod +x ./PROGRAMMES/*
chmod +x script_GONE.sh
```

## Input Requirements

- PLINK format files (.map and .ped)
- Maximum 1,800 individuals per analysis
- One population at a time
- INPUT_PARAMETERS_FILE with analysis settings

## Running GONE

```bash
bash script_GONE.sh input
```
Where "input" is your filename prefix (e.g., for input.map and input.ped)

## Output Files

- TEMPORARY_FILES directory with intermediate files
- Output_Ne_input: Ne estimates per generation
- Output_d2_input: Linkage disequilibrium values
- timefile: Analysis progress log

## Example Parameters

INPUT_PARAMETERS_FILE settings:
```
PHASE=2               # Phase information (0=pseudohaploids, 1=known, 2=unknown)
cMMb=1               # cM/Mb rate if genetic distances unknown
DIST=1               # Distance correction (0=none, 1=Haldane, 2=Kosambi)  
NGEN=2000            # Number of generations analyzed
NBIN=400             # Number of bins
MAF=0.0              # Minimum allele frequency
ZERO=1               # Allow ungenotyped SNPs
maxNCHROM=-99        # Maximum chromosomes (-99=all)
maxNSNP=50000        # SNPs per chromosome
hc=0.05              # Maximum recombination fraction
REPS=40              # Internal replicates
threads=-99          # Number of threads (-99=all)
```
## Visualization
[Click on me to take you to visualization guide](https://github.com/kkokay07/Pyplot-Hub/tree/main/Line%20plot)
## Citation

Santiago, E., Novo, I., Pardiñas, A. F. Saura, M., Wang, J., Caballero, A. (2020). Recent demographic history inferred by high-resolution analysis of linkage disequilibrium. Molecular Biology and Evolution 37: 3642–3653.

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
