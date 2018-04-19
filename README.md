# fast_downsample


Single python script for fast downsample fasta/fastq files to specific data size. Also works with gizp compressed files(*.gz)
The code requires python version after 3.5. No other environment is needed. 


## linux run example
```
python downsample.py --expected 10000000 --ifsort false --input /path-to-file/input.fasta --output /path-to-outdir/output.fasta
# --expected : number of base of result
# --ifsort : if the file is in order or not
# --input : input .fasta/.fastq/.gz data
# --output : oputput file, currently only supports output as .fatsq/.fasta
```

