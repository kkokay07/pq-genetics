**Step 1: Convert plink binary file to map and ped file**
```bash
./plink --bfile CDT_qc --recode --out cdt
```
**Step 2: Convert map and ped to eigenstrat format**
```bash
convertf -p par.PED.EIGENSTRAT
```
Format of par.PED.EIGENSTRAT is:
```bash
genotypename:    cdt.ped
snpname:         cdt.map 
indivname:       cdt.ped
outputformat:    EIGENSTRAT
genotypeoutname: cdt.geno
snpoutname:      cdt.snp
indivoutname:    cdt.ind
familynames:     NO
```
>Note: Ensure that .ind file is in following format. If not, convert using excel or similier software mannualy using .fam file
```bash
CHA_1	0	CHA
CHA_2	0	CHA
IDC_1	0	IDC
IDC_2	0	IDC
TIB_1	0	TIB
TIB_9	0	TIB
```
**Step 3: Run Alder**
```bash
/home/hp/Downloads/alder/alder -p alder_parameter_file.txt > alder_CHA_result.txt
```
Following is the alder_parameter_file.txt format
```bash
genotypename: cdt.geno
snpname: cdt.snp
indivname: cdt.ind
admixpop: CHA
refpops: TIB;IDC
raw_outname: alder_output_CHA_TIB
checkmap: NO
```


