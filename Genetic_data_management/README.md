
---

## **PLINK and VCFTools Commands for Genetic Data Formats**

### **1. Binary to `.map` and `.ped` Format**  
```bash
./plink --noweb --bfile name --cow --nonfounders --allow-no-sex --recode --out name
```

### **2. `.map` and `.ped` to Binary File**  
```bash
./plink --file yourdata --cow --make-bed --out outputfilename
```

### **3. `.map` and `.ped` to VCF File**  
```bash
./plink --cow --file name --recode vcf-iid --out name
./plink --ped name.ped --map MH_DFI.map --recode vcf --chr-set 29 --out name
```

### **4. VCF to `.map` and `.ped`**  
```bash
vcftools --vcf RTGMGL_phased.vcf --plink --out RTGMGLP
```

### **5. VCF to `.bed`, `.bim`, `.fam`**  
```bash
./plink --cow --allow-extra-chr --vcf pan.vcf --make-bed --out pan
```

### **6. Renaming Samples or Populations**  
```bash
./plink --cow --bfile allLoCaBreed_TOP_QC --fam rename.fam --make-bed --out Reordered
```

### **7. Indexing a VCF File**  
```bash
tabix -p vcf RTGMG_phased.vcf.gz
```
- **Output:** Generates a `.tbi` index file.

### **8. Compressing a VCF File**  
```bash
gzip -c GLGRCB.vcf > GLGRCB.vcf.gz
```

### **9. Imputation Using Beagle**  
```bash
java -jar beagle.22Jul22.46e.jar gt=phasing/pball.vcf out=phasing/pball_imputed
```

### **10. Extract Specific SNPs**  
**Input:** `.map` and `.ped`  
**Output:** Binary file  
```bash
./plink --noweb --file name --cow --extract mysnps.txt --allow-no-sex --make-bed --out name
```

### **11. Extract Specific Individuals**  
```bash
./plink --noweb --file data --cow --keep mylist.txt --make-bed --out name
```

**Example `mylist.txt`:**  
```plaintext
HOL    HOL_059
HOL    HOL_060
HR     Hr1
HR     Hr2
```

### **12. Filter Specific Populations**  
```bash
grep -E '^OG|^CB|^VW' all.txt > VWCBOG.txt
```

### **13. Merge Two Files**  
```bash
# Using PED and MAP files
./plink --cow --file data1 --merge data2.ped data2.map --make-bed --out merge

# Using Binary files
./plink --cow --bfile data1 --bmerge data2.bed data2.bim data2.fam --make-bed --out merge
```

### **14. Merge Multiple Files**  
**Example Command:**  
```bash
./plink --file fA --merge-list allfiles.txt --make-bed --out mynewdata
```

**`allfiles.txt`:** A list of files to merge, one set per row:  
```plaintext
fB.ped fB.map
fC.ped fC.map
fD.ped fD.map
fE.bed fE.bim fE.fam
fF.bed fF.bim fF.fam
fG.bed fG.bim fG.fam
fH.bed fH.bim fH.fam
```

---
