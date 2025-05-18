**Step 1: Make seperate chr wise files**
```bash
bash /home/hp/Downloads/shapeit.v2.904.3.10.0-693.11.6.el7.x86_64/bin/chr_hunter.sh
```
>Note: Download chr_hunter.sh and add correct file path of plink and change chr numbers as per your data

**Step 2: Phase data in shapeit (dont forget to add --force) (chromosome wise we need to run)**
```bash
/home/hp/Downloads/shapeit.v2.904.3.10.0-693.11.6.el7.x86_64/bin/shapeit --input-bed cdt1.bed cdt1.bim cdt1.fam --force -O cdt1
```
**Step 3: Prepare input files (.haps and .recomrates) for chromopainter2  (make run_imputetocp.sh and run in terminal)***
```bah
bash /home/hp/Downloads/shapeit.v2.904.3.10.0-693.11.6.el7.x86_64/bin/run_imputetocp.sh
```
>Note: we need map.txt file for all chr in the analysis. following is the format
```bash
pos	chr	cM
52854	1	0.052854
81978	1	0.081978
```
