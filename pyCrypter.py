#!/usr/bin/env python3

import pyAesCrypt
from getpass import getpass
from os import stat, remove
import sys
import argparse

bufferSize = 64 * 1024  # encryption/decryption buffer size - 64K


def main():
    parser = argparse.ArgumentParser(
        description='A Script to encrypt and decrypt files using pyAesCrypt')
    parser.add_argument(
        '-a',
        '--action',
        choices=['enc', 'dec'],
        required=True,
        help='Choose between enc for encrypt and dec for decryption')
    parser.add_argument('-i', '--ifile', required=True)
    parser.add_argument('-o', '--ofile', required=True)
    parser.add_argument('-s',
                        '--safe-mode=',
                        required=False,
                        choices=['True', 'False'],
                        default='False',
                        help='True will remove the plaintext file')

    global args
    args = parser.parse_args()

    if args.action == 'enc':
        encryptFile()
    elif args.action == 'dec':
        decryptFile()


# encrypt
def encryptFile():
    password = getpass()
    with open(args.ifile, "rb") as fIn:
        with open(args.ofile, "wb") as fOut:
            pyAesCrypt.encryptStream(fIn, fOut, password, bufferSize)
            if args.s == 'True':
                remove(args.ifile)


# decrypt
def decryptFile():
    password = getpass()
    encFileSize = stat(args.ifile).st_size  # get encrypted file size
    with open(args.ifile, "rb") as fIn:
        try:
            with open(args.ofile, "wb") as fOut:
                # decrypt file stream
                pyAesCrypt.decryptStream(fIn, fOut, password, bufferSize,
                                         encFileSize)
        except ValueError:
            print('Error')
            remove(args.ofile)  # remove output file on error


if __name__ == "__main__":
    main()