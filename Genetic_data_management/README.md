---

### **PLINK Commands for Genetic Data Management**

---

### **1. Binary to `.map` and `.ped` Format**  
**Input:** Binary file (`input.bed`, `input.bim`, `input.fam`)  
**Output:** `.map` and `.ped` files  
```bash
./plink --noweb --bfile input --cow --nonfounders --allow-no-sex --recode --out output
```

---

### **2. `.map` and `.ped` to Binary File**  
**Input:** `.map` and `.ped` files  
**Output:** Binary file (`output.bed`, `output.bim`, `output.fam`)  
```bash
./plink --file input --cow --make-bed --out output
```

---

### **3. `.map` and `.ped` to VCF File**  
**Input:** `.map` and `.ped` files  
**Output:** VCF file (`output.vcf`)  
```bash
./plink --cow --file input --recode vcf-iid --out output
```

---

### **4. VCF to `.map` and `.ped`**  
**Input:** VCF file (`input.vcf`)  
**Output:** `.map` and `.ped` files  
```bash
vcftools --vcf input.vcf --plink --out output
```

---

### **5. VCF to `.bed`, `.bim`, `.fam`**  
**Input:** VCF file (`input.vcf`)  
**Output:** Binary file (`output.bed`, `output.bim`, `output.fam`)  
```bash
./plink --cow --allow-extra-chr --vcf input.vcf --make-bed --out output
```

---

### **6. Renaming Samples or Populations**  
**Input:** Binary file (`input.bed`, `input.bim`, `input.fam`)  
**Output:** Renamed binary file (`output.bed`, `output.bim`, `output.fam`)  
```bash
./plink --cow --bfile input --fam rename.fam --make-bed --out output
```

---

### **7. Extract Specific SNPs**  
**Input:** SNP list file (`mysnps.txt`), `.map`, and `.ped` files  
**Output:** Binary file (`output.bed`, `output.bim`, `output.fam`)  
```bash
./plink --noweb --file input --cow --extract mysnps.txt --allow-no-sex --make-bed --out output
```

**Format of `mysnps.txt`:**  
```plaintext
rs12345
rs67890
rs112233
```

---

### **8. Extract Specific Individuals**  
**Input:** Individual list file (`mylist.txt`), `.map`, and `.ped` files  
**Output:** Binary file (`output.bed`, `output.bim`, `output.fam`)  
```bash
./plink --noweb --file input --cow --keep mylist.txt --make-bed --out output
```

**Format of `mylist.txt`:**  
```plaintext
F1    IID1
F2    IID2
F3    IID3
```

---

### **9. Merge Two Files**  
**Input:** Two datasets (`data1`, `data2`)  
**Output:** Merged binary file (`output.bed`, `output.bim`, `output.fam`)  
```bash
# Using PED and MAP files
./plink --cow --file data1 --merge data2.ped data2.map --make-bed --out output

# Using Binary files
./plink --cow --bfile data1 --bmerge data2.bed data2.bim data2.fam --make-bed --out output
```

---

### **10. Merge Multiple Files**  
**Input:** List of files in `merge_list.txt`  
**Output:** Merged binary file (`output.bed`, `output.bim`, `output.fam`)  
```bash
./plink --cow --file file1 --merge-list merge_list.txt --make-bed --out output
```

**Format of `merge_list.txt`:**  
```plaintext
file2.ped file2.map
file3.ped file3.map
file4.bed file4.bim file4.fam
```

---
