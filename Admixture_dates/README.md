**Step 1: Make seperate chr wise files**
```bash
bash /home/hp/Downloads/shapeit.v2.904.3.10.0-693.11.6.el7.x86_64/bin/chr_hunter.sh
```
>Note: Download chr_hunter.sh and add correct file path of plink and change chr numbers as per your data

**Step 2: Phase data in shapeit (dont forget to add --force) (chromosome wise we need to run)**
```bash
/home/hp/Downloads/shapeit.v2.904.3.10.0-693.11.6.el7.x86_64/bin/shapeit --input-bed cdt1.bed cdt1.bim cdt1.fam --force -O cdt1
```
