import gnupg
import os

gpghome = os.getenv('GNUPG_HOME', f'{os.getenv("HOME")}/.gnupg')

gpg = gnupg.GPG(gnupghome=gpghome)
gpg.encoding = 'UTF-8'

def import_publickey(publickey: str):
  import_result = gpg.import_keys(publickey)
  return import_result 

def get_fingerprints(publickey: str):
  fingerprints = gpg.scan_keys_mem(publickey).fingerprints
  return fingerprints

def encrypt_message(message: str, recepient: str):
  return gpg.encrypt(message, recepient, always_trust=True)

def get_recipients(message: str):
  return gpg.get_recipients(message)

def delete_publickey(fingerprint: str):
  return gpg.delete_keys(fingerprint)
