from hashlib import pbkdf2_hmac as pbkdf2
from secrets import choice, token_bytes
from json import loads, dumps
from subprocess import Popen, PIPE, STDOUT
from pathlib import PosixPath
from dataclasses import dataclass
from string import printable

__all__ = []

def openssl(*args,b=b''):
    cmd = ['openssl', *args]
    p = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=STDOUT)
    return p.communicate(b)[0]

@dataclass
class Item:
    pk: bytes
    data: bytes
    iv: bytes
    salt: bytes

    @property
    def packed(self):
        return b','.join([self.pk, self.data, self.iv, self.salt])

class Engine:
    def __init__(self, filepath, xor=False):
        self._filepath = PosixPath(filepath)
        if not self._filepath.is_file():
            self._init_db()
        self._do_xor = xor
        self._items = []

    def _init_db(self):
        self._filepath.touch(exist_ok=True)

    def _decrypt(self, ct, iv, salt, dk):
        return openssl('enc','-aes256','-d','-K',dk.hex(),'-iv',iv.hex(),'-S',salt.hex(),b=ct)

    def _encrypt(self, pt, iv, salt, dk):
        return openssl('enc','-aes256','-e','-K',dk.hex(),'-iv',iv.hex(),'-S',salt.hex(),b=pt)

    def _derive_key(self, pw):
        self._dk = pbkdf2('sha256', pw.encode('ascii'), pw[::-3].encode('ascii'), 12000)

    def _xor(self, k, x):
        '''
        Byte-for-byte xor of x by k
        '''
        # FIXME
        r = ''
        p = 0
        for i, c in enumerate(x):
            r += chr(c ^ k[p])
            p = (p < len(k)-1)*p + (p < len(k)-1)*1
        breakpoint()
        return bytes(r)

    def _new_secret(self, secret_id, secret):
        '''
        iv, salt, key chosen at random
        '''
        salt = ''.join([choice(printable) for x in range(8)])
        salt.encode('ascii')
        iv = token_bytes(16)
        hash(secret_id+salt)
        pass

    def _add_item(self, *args):
        assert [type(a) is bytes for a in args],f"{args} must be bytes"
        self._items.append(Item(*args))

    def _read_db(self):
        with open(self._filepath, 'rb') as f:
            data = f.read()
        if data != b'':
            breakpoint()
            # we probably should validate data
            if self._do_xor:
                data = self._xor(self._dk, data)
            r = [ x for x in data.split(b',,') if x not in [b'', b'\n'] ]
            if len(r) > 0:
                for row in r:
                    self._items.append(Item(*row.split(b',')))

    def _write_db(self):
        # we probably should copy file to .bak
        r = [ c.packed for c in self._items ]
        data = b',,'.join(r)
        breakpoint()
        if self._do_xor:
            data = self._xor(self._dk, data)
        with open(self._filepath, 'wb') as f:
            f.write(data)
    
    def _get_secret(self, s):
        raise NotImplementedError

    def _new_secret(self, s):
        raise NotImplementedError

    def get_secret(self, s):
        # present the secret
        return self._decrypt(s)

class Keys(Engine):
    '''
    key_a is chosen at random
    iv_a is chosen at random
    salt_a is chosen at random
    secret_id is a string like 'mysecret'
    id_a = hash(secret_id+salt_a)
    enc_m(key_a) = openssl -iv iv_a -e -aes256 -K key_m -p password? -S salt_a

    /*******************************\
    | id_a:enc_m(key_a):salt_a:iv_a |
    \*******************************/
    '''

    def _get_secret(self, s):
        pass

    def _new_secret(self, s):
        pass

class Secrets(Engine):
    '''
    key_a is the key material decrypted from key_db
    id_a is the id from keys.db
    id_sa = hash(key_a+id_a)
    secret is the secret text like 'this is the secret'
    enc_a(secret) = openssl -iv iv_sa -e -aes256 -K key_a -p password? -S salt_sa

          secrets.db
          
    /************************************\
    | id_sa:enc_a(secret):salt_sa:iv_sa |
    \************************************/

    '''
    def _get_secret(self, s):
        pass

    def _new_secret(self, s):
        pass

class SecretEngine:
    def __init__(self):
        # name of db
        # master key
        pass

    def create(self, s):
        # tell keys you want to make a new secret with secret_id
        # tell secret you want to make a new secret with secret
        pass

    def read(self, s):
        # tell keys the secret_id you want, and the derived key
        # keys tells secrets about the key for the secret you want
        # secrets tells you about the key you asked for

        # key is not tried until secret requested
        # name of secret
        pass

    def update(self, s):
        pass

    def delete(self, s):
        pass

    def provide_master_key(self, m):
        pass
__all__ += ['SecretEngine']
