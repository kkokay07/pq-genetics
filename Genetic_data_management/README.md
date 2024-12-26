---

## **PLINK Commands for Genetic Data Management**

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
**Input:** Binary file (`input.bed`, `input.bim`, `input.fam`) and `rename.fam`  
**Output:** Binary file with updated IDs (`output.bed`, `output.bim`, `output.fam`)  
```bash
./plink --cow --bfile input --fam rename.fam --make-bed --out output
```

**Example `rename.fam` Format:**  
```plaintext
FId1 IID1 New_FId1 New_IID1
FId2 IID2 New_FId2 New_IID2
```

---

### **7. Extract Specific SNPs**
**Input:** `.map` and `.ped` files, SNP list (`mysnps.txt`)  
**Output:** Binary file (`output.bed`, `output.bim`, `output.fam`)  
```bash
./plink --noweb --file input --cow --extract mysnps.txt --allow-no-sex --make-bed --out output
```

**Example `mysnps.txt` Format:**  
```plaintext
rs12345
rs67890
rs54321
```

---

### **8. Extract Specific Individuals**
**Input:** `.map` and `.ped` files, individual list (`mylist.txt`)  
**Output:** Binary file (`output.bed`, `output.bim`, `output.fam`)  
```bash
./plink --noweb --file input --cow --keep mylist.txt --make-bed --out output
```

**Example `mylist.txt` Format:**  
```plaintext
FId1 IID1
FId2 IID2
```

---

### **9. Merge Two Files**
**Input:** Two datasets in `.map` and `.ped` format  
**Output:** Merged binary file (`output.bed`, `output.bim`, `output.fam`)  
```bash
./plink --cow --file data1 --merge data2.ped data2.map --make-bed --out output
```

**Input:** Two datasets in binary format  
**Output:** Merged binary file (`output.bed`, `output.bim`, `output.fam`)  
```bash
./plink --cow --bfile data1 --bmerge data2.bed data2.bim data2.fam --make-bed --out output
```

---

### **10. Merge Multiple Files**
**Input:** List of files to merge (`merge_list.txt`)  
**Output:** Merged binary file (`output.bed`, `output.bim`, `output.fam`)  
```bash
./plink --file input --merge-list merge_list.txt --make-bed --out output
```

**Example `merge_list.txt` Format:**  
```plaintext
file1.ped file1.map
file2.ped file2.map
file3.bed file3.bim file3.fam
file4.bed file4.bim file4.fam
```

---
```
