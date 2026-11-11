"""Optional password-encrypted SQLite export, entirely on the local machine.

This is NOT encryption at rest: the running project's existing instance DB is
still plaintext SQLite. Never store backup passphrases or decrypted contents.
"""
import hashlib
import os
import sqlite3
from pathlib import Path
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from config.settings import DB_PATH

MAGIC=b'HIA-SECURE-BACKUP\x01'
MAX_SIZE=70*1024*1024


def _key(secret:str,salt:bytes)->bytes:
    if not isinstance(secret,str) or len(secret)<12 or len(secret)>256:
        raise ValueError('Backup passphrase must be 12-256 characters.')
    return hashlib.scrypt(secret.encode('utf-8'),salt=salt,n=2**14,r=8,p=1,dklen=32)


def snapshot_database_bytes(path:Path=DB_PATH)->bytes:
    """Use SQLite backup API for a consistent snapshot even in WAL mode."""
    if not path.is_file():
        raise ValueError('No local database to back up.')
    if path.stat().st_size>MAX_SIZE:
        raise ValueError('Database exceeds the offline backup size limit.')
    with sqlite3.connect(f'file:{path.as_posix()}?mode=ro',uri=True) as original:
        with sqlite3.connect(':memory:') as snapshot:
            original.backup(snapshot)
            data=snapshot.serialize()
    if len(data)>MAX_SIZE:
        raise ValueError('Database snapshot is too large to export.')
    return data


def encrypt_database(secret:str,path:Path=DB_PATH)->bytes:
    plaintext=snapshot_database_bytes(path)
    salt=os.urandom(16);nonce=os.urandom(12)
    header=MAGIC+salt+nonce
    return header+AESGCM(_key(secret,salt)).encrypt(nonce,plaintext,header)


def decrypt_database(payload:bytes,secret:str)->bytes:
    prefix=len(MAGIC)
    if not payload.startswith(MAGIC) or len(payload)<prefix+16+12+16 or len(payload)>MAX_SIZE+1024:
        raise ValueError('Invalid or oversized encrypted backup.')
    salt=payload[prefix:prefix+16];nonce=payload[prefix+16:prefix+28]
    header=payload[:prefix+28]
    try:
        raw=AESGCM(_key(secret,salt)).decrypt(nonce,payload[prefix+28:],header)
    except Exception as exc:
        raise ValueError('Incorrect passphrase or corrupted backup.') from exc
    with sqlite3.connect(':memory:') as check:
        try:
            check.deserialize(raw)
            if check.execute('PRAGMA quick_check').fetchone()[0]!='ok':
                raise ValueError('Database integrity check failed.')
        except sqlite3.DatabaseError as exc:
            raise ValueError('The decrypted data is not a valid SQLite database.') from exc
    return raw


def restore_as_new_file(payload:bytes, secret:str, output:Path):
    """Only create a NEW output; never overwrite any live database."""
    output=Path(output)
    if output.exists():
        raise FileExistsError('Restore destination already exists: choose a new filename.')
    raw=decrypt_database(payload,secret)
    output.parent.mkdir(parents=True,exist_ok=True)
    try:
        with sqlite3.connect(':memory:') as src:
            src.deserialize(raw)
            with sqlite3.connect(output) as dst:
                src.backup(dst)
    except Exception:
        output.unlink(missing_ok=True)
        raise
