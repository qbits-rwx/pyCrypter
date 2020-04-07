#!/usr/bin/env python3

import pyAesCrypt
from getpass import getpass
from os import stat, remove
import sys, getopt

bufferSize = 64 * 1024 # encryption/decryption buffer size - 64K
password = getpass()
# plainData = sys.argv[2]
# plainData = "test.txt"
# encData = "cipher.txt"

def main(argv):
    plainFile  = ''
    encFile  = ''
    try:
        opts,args = getopt.getopt(argv,"hi:o:",["plainFile=","encFile="])
    except getopt.GetoptError:
        print ('pyCrypt.py -i <inputfile> -o <outputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print ('pyCrypt.py -i <inputfile> -o <outputfile>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            plainFile = arg
        elif opt in ("-o", "--ofile"):
            encFile = arg

    action = sys.argv[1] # enc || dec

    if action in 'enc':
        encryptFile()
    elif action in 'dec':
        decryptFile()

# encrypt
def encryptFile():
  with open(plainFile, "rb") as fIn:
    with open(encFile, "wb") as fOut:
        pyAesCrypt.encryptStream(fIn, fOut, password, bufferSize)
  remove(plainFile)

# decrypt
def decryptFile():
  encFileSize = stat(ifile).st_size # get encrypted file size
  with open(ofile, "rb") as fIn:
    try:
        with open("test.txt", "wb") as fOut:
            # decrypt file stream
            pyAesCrypt.decryptStream(fIn, fOut, password, bufferSize, encFileSize)
    except ValueError:
        print('Error')
        remove("cipher.txt") # remove output file on error

if __name__=="__main__":
    main(sys.argv[1:])