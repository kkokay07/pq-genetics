# README

## 🧬 Local Ancestry Analysis Notebook

### Overview
This notebook, `LAAN_(local_ancestry_analysis_notebook).ipynb`, helps analyze local ancestry in genomic data. It works smoothly on **Google Colab**, so no installations are needed!

### 🚀 How to Use on Google Colab
1. **Open the Notebook**  
   - DClick on "LAAN_(local_ancestry_analysis_notebook).ipynb"
   - Click on "Open in Colab" at top left corner.

2. **Load Your Data**  
   - Create a folder in the google drive and upload your plink binary files (.bed/.bim/.fam). (Dont create inside any other folders in drive! If you do so, then dont forget to specify the path in step 1)
   - Download "tools_local_ancestry" folder and simply upload it to your google drive. (Dont upload inside any other folders in drive!)
   - In Step 1 code, ensure the PROJECT_FOLDER and TOOLS_FOLDER paths are correct. 
  
3. **Run the Notebook**  
   - Execute cells one by one.
   - In Step 4, find the following lines and set the anc_threshold and target_threshold as you desire. Default values are set to 0.75 and 0.9 respectively
          # ------------------------------
          # Step: Filter Individuals Based on Composition Thresholds (K=3)
          # ------------------------------
          anc_threshold = 0.75    # For ancestral groups, require proportion >= 0.75
          target_threshold = 0.90 # For target, remove if proportion > 0.90

### 🎯 Expected Output
- Processed ancestry data.
- Clear visualizations of ancestry patterns.
- Summary statistics.

### 🛠 Troubleshooting
- Check if file paths are correct.
- Rerun the first few cells if an error occurs.


## 👨‍🔬 About the Author

**Dr. Kanaka K. K., PhD, ARS**  
Scientist  
School of Bioinformatics and Computational Biology
[ICAR-Indian Institute of Agricultural Biotechnology, Ranchi](https://iiab.icar.gov.in/)
> [Be like IIAB!:](https://www.researchgate.net/publication/379512649_ICAR-IIAB_Annual_Report-_2023) IIAB is like yogic center where all the sciences (Plant, Animal, Aquatic,Mibrobiology, IT) meet to address emerging issues in food production.

## 🔎 Spy on me
- [Google Scholar](https://scholar.google.com/citations?hl=en&user=0dQ7Sf8AAAAJ&view_op=list_works&sortby=pubdate)
- [GitHub: kkokay07](https://github.com/kkokay07)
- [ResearchGate](https://www.researchgate.net/profile/Kanaka-K-K/research)
- [Institute Website](https://iiab.icar.gov.in/staff/dr-kanaka-k-k/)
