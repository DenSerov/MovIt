#!/usr/bin/python
from os import name as os_name
from os import listdir
from os import mkdir
from os import rename
from os import chdir
from os import getcwd
from os import walk
from time import sleep
from time import ctime
from subprocess import Popen
from sys import argv

import boto3


if len(argv) < 4:
    print("Usage syntax:")
    if os_name == "nt":
        print(argv[0].split('\\')[-1],"[input path] [output path] [basecal script]")
    else:
        print(argv[0].split('/')[-1],"[input path] [output path] [basecal script]")
    print("Example [Default]:")
    print("mover.py ./genome_new ./genome_processing basecal.py")
    print("Trying to use above defaults")
    sleep(1)
    genome_new = "./genome_new"
    genome_processing = "./genome_processing"
    basecal = "basecal.py"

if len(argv) == 4:
    genome_new = argv[1]
    genome_processing = argv[2]
    basecal = argv[3]


def mover():
    print(ctime(), "Mover is checking for FAST5 files")
    folder = []
    for entry in walk(genome_new):
        folder.append(entry)
    for address, dirs, files in folder:
        for f in files:
            # print(address, f)
            if "fast5" in f:
                destination = address.replace('new', 'processing')
                rename(address, destination)
                break

    folder = []
    for entry in walk(genome_processing):
        folder.append(entry)

    for address, dirs, files in folder:
        for d in dirs:
            print(ctime(), "Launching base call for FAST5 Seq_ID", d[-5:])
            # print(address+'\\'+d)
            target = address+'\\'+d
            Popen('python basecall.py %s' % (target,), shell=True)
            sleep(2)
    return True


mypath = '"'+getcwd() + "\\" + basecal + '"'

while True:
    mover()
    sleep(5)
#    exit(0)
