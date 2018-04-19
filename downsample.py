import random
import sys
import gzip
import argparse
import subprocess


def lowcov(f, type, f_out):
    # no enough data
    with open(f_out, "w") as output:
        if type == "gz":
            with gzip.open(f, "rt") as myfile:
                for line in myfile:
                    output.write(line)
                output.close()
                sys.exit()
        else:
            with open(f, "r") as myfile:
                for line in myfile:
                    output.write(line)
                output.close()
                sys.exit()


def downsample(expected, ifsort, f, f_out):
    filetype = f.split(".")[-1]

    # r is the read length, i.e. how many base in 1 read
    if filetype in ['fq', 'fastq', 'fasta', 'fa']:
        # uncompressed file
        myfile = open(f, "r")
        x = myfile.readline()  # skip first line
        r = len(myfile.readline()) - 1  # read length

        # with open(f, "r") as input:
        #     file_len = len(input.readlines())
        process = subprocess.Popen(['wc', '-l', f], stdout=subprocess.PIPE)
        stdout = process.communicate()[0]
        file_len=int(stdout.split()[0].decode("utf-8", "ignore"))

    elif filetype == 'gz':
        # compressed file
        filetype = f.split('.')[-2] #reset file type
        myfile = gzip.open(f, "rt")
        x = myfile.readline()  # skip first line
        r = len(myfile.readline()) - 1

        # with open(f, "r") as input:
        #     file_len = len(input.readlines())
        p1 = subprocess.Popen(['zcat', f], stdout=subprocess.PIPE)
        p2 = subprocess.Popen(['wc', '-l'], stdin=p1.stdout, stdout=subprocess.PIPE)
        stdout = p2.communicate()[0]
        file_len=int(stdout.split()[0].decode("utf-8", "ignore"))
    else:
        sys.exit('file type is not supported {}'.format(f.split(".")[-2:]))


    # get probabilities
    if filetype in ['fq', 'fastq']:
        p = (expected / r) / file_len * 4.  # calculated expected probability based on #lines
        print("Probability is {} \n b contained is {}".format(p, r*file_len/4.))
    elif filetype in ['fa', 'fasta']:
        p = (expected / r) / file_len * 2. # calculated expected probability based on #lines
        print("Probability is {} \n b contained is {}".format(p, r * file_len / 2.))

    # if expected data is larger than original contains, no downsampling is performed
    if p > 1:
        lowcov(f, f.split(".")[-1], f_out)
        print("No down sample is performed on {}, file length is {}".format(f_out, file_len))

    output = open(f_out, 'w')  # open the output file

    if ifsort.lower() in ['f', 'fasle']:
        # if not sorted, pick first x lines of file is enough
        if f.split()[-1] != "gz":
            process = subprocess.Popen(['head', '-{}'.format(expected), f], stdout=subprocess.PIPE)
            stdout = process.communicate()[0].decode("utf-8", "ignore")
            with open(f_out, 'w') as myfile:
                myfile.write(stdout)
        else:
            p1 = subprocess.Popen(['zcat', f], stdout=subprocess.PIPE)
            p2 = subprocess.Popen(['head', '-{}'.format(expected)], stdin=p1.stdout, stdout=subprocess.PIPE)
            stdout = p2.communicate()[0].decode("utf-8", "ignore")
            with open(f_out, 'w') as myfile:
                myfile.write(stdout)

    elif ifsort.lower() in ['t', 'true']:
        # if sorted, perform random downsample
        if filetype in ['fq', 'fastq']:
            i = 0
            inOrNot = True
            for line in myfile:
                if i % 4 == 0:
                    inOrNot = random.random() <= p
                if (inOrNot):
                    output.write(line)
                i += 1

        elif filetype in ['fa', 'fasta']:
            for line in myfile:
                # p = expected/(len(lines)*len(lines[1]))
                out = ''
                # for line in lines:
                if line[0] == ">":
                    out = line
                    if random.random() <= p:
                        output.write(out)
                else:
                    out += line

        myfile.close()
        output.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser("Random downsample sequencing file:")
    parser.add_argument("--expected", help="expected of total amount of nucleotides", type=int, default=10 ** 7)
    parser.add_argument("--ifsort", help="if the sequence file is sorted or random, T/t/True/true or F/f/False/false", type=str)
    # parser.add_argument("--len", help="# file line by $(wc -l $file)", type=int)
    parser.add_argument("--input", help="# input file", type=str)
    parser.add_argument("--output", help="# output file", type=str)
    args = parser.parse_args()

    downsample(args.expected, args.ifsort, args.input, args.output)
