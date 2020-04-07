#!/usr/bin/env python3

import pyAesCrypt
from getpass import getpass
from os import stat, remove
import sys

bufferSize = 64 * 1024 # encryption/decryption buffer size - 64K
password = getpass()
#plainData = sys.argv[2]
plainData = "test.txt"
encData = "cipher.txt"

def main():
    action = sys.argv[1] # enc || dec
#   if action not in 'enc' or 'dec':
#        print(sys.argv[1])
#        print(sys.argv[0] + ' ' + 'use enc | dec  as an option')
    if action in 'enc':
        encryptFile()
    elif action in 'dec':
        decryptFile()

# encrypt
def encryptFile():
  with open("test.txt", "rb") as fIn:
    with open("cipher.txt", "wb") as fOut:
        pyAesCrypt.encryptStream(fIn, fOut, password, bufferSize)
  remove("test.txt")

# decrypt
def decryptFile():
  encFileSize = stat("cipher.txt").st_size # get encrypted file size
  print(encFileSize)
  with open("cipher.txt", "rb") as fIn:
    try:
        with open("test.txt", "wb") as fOut:
            # decrypt file stream
            pyAesCrypt.decryptStream(fIn, fOut, password, bufferSize, encFileSize)
    except ValueError:
        print('Error')
        remove("cipher.txt") # remove output file on error

if __name__=="__main__":
    main()