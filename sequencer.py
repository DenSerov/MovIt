#!/usr/bin/python
from sys import argv
from os import mkdir
from time import sleep
from time import time
from os import chdir
from subprocess import call

if len(argv) == 1:
    print("Usage syntax:")
    print(argv[0],"[nfs | rsync] [genomes qty] [files per genome] [delay] [final destination path]")
    exit(0)

output_dir = argv[5]
output_len = int(argv[3])
output_qty = int(argv[2])
delay = int(argv[4])

if argv[1] == 'nfs':
    NFS = True
    rsync = False
elif argv[1] == 'rsync':
    NFS = False
    rsync = True


def file_creator(n, index):
    if index >= 0:
        name = "seq_" + str(n) + "." + str(index) + ".fast5"
    else:
        name = "seq_" + str(n) + ".finish"

    if NFS:
        name = "nfs_"+str(n)+"/"+name
    if rsync:
        name = "rsy_"+str(n)+"/"+name

    f = open(name, mode='w')
    f.close()

    return

if NFS:
    chdir(output_dir)
if rsync:
    chdir('./fast5')

for j in range(output_qty):
    print("Preparing FAST5 sequence", j+1, "of", output_qty)
    files_to_create = output_len
    seq_id = str(int(time()))[4:]
    print("Seq_ID:", seq_id)

    if NFS:
        mkdir('nfs_' + seq_id)
    if rsync:
        mkdir('rsy_' + seq_id)

    for i in range(files_to_create):
        file_creator(seq_id, i)
    file_creator(seq_id, -1)
    sleep(delay)

    if rsync:
        print("Calling RSYNC to copy contents to ONTAP NFS share")
        call("rsync -r /home/sequenator/fast5/* "+output_dir, shell=True)
        call("rm -rf /home/sequenator/fast5/*", shell=True)
