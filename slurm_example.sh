#!/bin/bash


# example for submit job on slurm cluster
name=downsample_test
mem=8
days=1
cwd=$(pwd)
logdir=$cwd/log
mkdir -p logdir

# change input file here
in=input.fasta 


id=$(sbatch \
--ntasks=1 \
--cpus-per-task=1 -N 1 \
--job-name=$name \
--mem=${mem}000 \
--time=${days}-0 \
--out=${logdir}/${name}.out \
--open-mode=append \
--wrap="python ${cwd}/downsample.py --expected 10000000 --ifsort f --input ${in} --output $(cut -d'.' -f1<<<$in)_downsampled.fasta")
echo $id
