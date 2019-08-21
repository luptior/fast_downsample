# fast_downsample


Single python script for fast downsample fasta/fastq files to specific data size. Also works with gizp compressed files(*.gz)
The code requires python version after 3.5. No other environment is needed. 


## linux run example
```sh
python downsample.py --expected 10000000 --ifsort false --input /path-to-file/input.fasta --output /path-to-outdir/output.fasta
# --expected : number of base of result
# --ifsort : if the file is in order or not
# --input : input .fasta/.fastq/.gz data
# --output : oputput file, currently only supports output as .fatsq/.fasta
```

## slurm submission script example
Pysbatch: https://github.com/luptior/pysbatch
```sh
# change the input file path and other variable in shell script if necessary
sh slurm_example.sh
python slurm_example.sh
```

## further
1. add support to upsample
2. simpler method for normalize a batch of sequence files to same size/depth
