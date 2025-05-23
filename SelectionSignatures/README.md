**STEP 1: Make population wise vcf file**
`
**Step 2: REMOVE * FROM THE VCF AND REPLACING IT WITH N**
```bash
for i in {1..28}
do
  sed 's/\*/N/g' Jmchr_chr${i}.vcf.gz > Jmchr_chr${i}_fixed.vcf
done
```
**Step 3: 
