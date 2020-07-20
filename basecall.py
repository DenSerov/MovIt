#!/usr/bin/python

genome_processing = "L:\genome.processing"
genome_finished = "L:\genome.finished"

#genome_new = ".\\genome.new"
#genome_processing = ".\\genome.processing"
#genome_finished = ".\\genome.finished"

from sys import argv
from time import sleep
from time import ctime
from os import chdir
from os import getcwd
from os import listdir
from os import rename


def base_call(fast5):
    fastq = workdir+"\\"+fast5[:-1]+"q"
    print(ctime(), "Generating FASTQ:", fastq)
    fastq_f = open(fastq, "w")
    # BASE CALL LOGIC HERE
    sleep(0.2)
    fastq_f.close()
    return

print("BASECALL for ",argv[1],"LAUNCHED")
workdir = argv[1]
print(workdir)
files = listdir(workdir)
print(files)
for f in files:
    if '5' in f[-1]:
        base_call(f)
        print(f, "is processed.\n\n")
        sleep(0.1)
print(ctime(), "Finished processing", len(files), "files.")
destination =  workdir.replace('processing','finished')
print(workdir,'=>',destination)
rename(workdir,destination)
print(ctime(), "Closing ...")
sleep(1)
