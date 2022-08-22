import os
from hashlib import pbkdf2_hmac as pbkdf2
from secrets import choice, token_bytes
from json import loads, dumps
from subprocess import Popen, PIPE, STDOUT
from pathlib import PosixPath
from dataclasses import dataclass
from string import printable
from sys import maxsize

def openssl(*args,b=b''):
    cmd = ['openssl', *args]
    p = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=STDOUT)#, pass_fds=(fdr))
    breakpoint()
    return p.communicate(b)[0]
    
def _decrypt(iv, salt, dk, ct):
    return openssl('enc','-aes256','-d','-K',dk.hex(),'-iv',iv.hex(),'-S',salt.hex(),b=ct)

def _encrypt(iv, salt, dk, pt):
    return openssl('enc','-aes256','-e','-K',dk.hex(),'-iv',iv.hex(),'-S',salt.hex(),b=pt)

def main():

    pw = 'meatman'

    secret_id = 'test_id'

    dk = pbkdf2('sha256', pw.encode('ascii'), pw[::-3].encode('ascii'), 12000)

    #salt = ''.join([choice(printable) for x in range(8)])
    salt = 'ssssssss'
    pkey = (hash(secret_id+salt) & maxsize).to_bytes(8, 'big') 

    skey = token_bytes(256)

    #iv = token_bytes(32)
    iv = b'c'*16
    salt = salt.encode('ascii')

    ct = _encrypt(iv, salt, dk, b"this is a test")
    pt = _decrypt(iv, salt, dk, ct)

if __name__ == '__main__':
    main()
