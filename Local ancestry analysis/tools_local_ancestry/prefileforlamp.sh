#BASH SCRIPT:
#!/bin/bash

CHR=$1
outfile=$2

#mkdir CHR${CHR}
#cd CHR${CHR}


## make LAMP input file
cat  ${outfile}_CHR${CHR}.raw | awk 'NR > 1' | cut -d' ' -f 7- | sed 's/NA/-1/g' > ${outfile}_CHR${CHR}_LAMPGENO.txt
cat ${outfile}_CHR${CHR}.bim | awk '{print $4}' > ${outfile}_CHR${CHR}_LAMPMAP.txt

echo "populations=2
pfile=purebred_BI_CHR${CHR}.prob,purebred_BT_CHR${CHR}.prob
ancestralsamplesize=30,73
genofile=GENOTYPES
posfile=SNPPOSITION
outputancestryfile=OUTFILE
offset=0.2
recombrate=1e-8
generations=02
alpha=0.60,0.4
ldcutoff=1" > config.txt

#### MAKE LAMP configeration file
cat config.txt | awk -v G=${outfile}_CHR${CHR}_LAMPGENO.txt -v M=${outfile}_CHR${CHR}_LAMPMAP.txt -v O=${outfile}_CHR${CHR}_results.txt '{gsub(/GENOTYPES/,G);gsub(/SNPPOSITION/,M);gsub(/OUTFILE/,O); print}' \
>  ${outfile}_CHR${CHR}configfile.txt


### runing LAMP
#lamp ${outfile}_CHR${CHR}configfile.txt

#cd ..

#------------------------------------------
