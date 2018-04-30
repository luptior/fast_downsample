from pysbatch import *

name="downsample_test"
input="input.fasta"

wrap=f"python downsample.py --expected 10000000 --ifsort f --input ${input} --output downsampled_${input}"

sbatch(job_name=name, mem=8, time=1-0, log="submit.out", wrap=wrap, add_option="--open-mode=append")
