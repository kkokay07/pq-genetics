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
**Step 4: Estimate 'n' and 'm'(looped in run_ChromoPainterv2.sh)**
```bash
bash /home/hp/Documents/Admixture_date/Chromopainter/Equal_samples/KAM/run_ChromoPainterv2.sh
```
>Note: This requires INDI.txt with following format (Here CHA should be in top. If I am running for IDC, then IDC individuals should be at top.)
```bash
CHA_1	CHA	1
CHA_2	CHA	1
CHA_3	CHA	1
CHA_4	CHA	1
IDC_1	IDC	1
IDC_2	IDC	1
IDC_2	IDC	1
TIB_1	TIB	1
TIB_2	TIB	1
```
>Note: This also need POPSURR.txt with following format (in this example I am using CHA as recipient. So focus on CHA carefully)

```bash
IDC	D
TIB	D
CHA	R
IDC	D
TIB	D
```
**Step 5: Finding out n and M value**
>Note: open .haps output file of step 3 and take SNP number which will be there in 2nd row and compile in ChromoPainterv2EstimatedNeExtractEM.pl in @chromovec and @chromolengths= )
```bash
perl /home/hp/Documents/Admixture_date/Chromopainter/All_sample_run_copy/ChromoPainterv2EstimatedNeMutExtractEM.pl
```
**Step 6: Generating the copy vector input file using n and M value got in previous step.** (looped in run_copy_vector_generater.sh)
```bash
bash /home/hp/Documents/Admixture_date/Chromopainter/All_sample_run_copy/run_copy_vector_generater.sh
```
>Note: Some time chr1.recomrates, will be with the extension chr1.recomfile

