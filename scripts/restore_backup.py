"""Restore a password-encrypted backup to a *new* SQLite file, never overwriting the live DB.

Usage (STOP Streamlit before any later manual migration):
 python -m scripts.restore_backup --input file.hiaenc --output E:\\safe\\restored-healthcare.db
"""
import argparse
from pathlib import Path
from getpass import getpass
from services.secure_backup import restore_as_new_file


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input',required=True)
    parser.add_argument('--output',required=True)
    args=parser.parse_args()
    password=getpass('Encrypted backup passphrase: ')
    restore_as_new_file(Path(args.input).read_bytes(),password,Path(args.output))
    print('Backup verified and restored into a NEW file:',args.output)
    print('The current application database was NOT modified.')

if __name__=='__main__': main()
