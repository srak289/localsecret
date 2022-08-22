from base64 import b64encode, b64decode
from os.path import abspath, dirname, join
from json import loads, dumps
from re import match

class Secrets:
    def __init__(self, path=f'{__file__}', key='/etc/hostname'):
        self.path = path
        self.__keyfile = keyfile

    def __secrets(self):
        return join(dirname(abspath(self.path)), '.secrets')
    
    def __key(self):
        try:
            with open(self.__keyfile, 'r') as f:
                a = f.read()
            return ''.join([x for x in a if match('[0-z]', x)])
        except:
            raise Exception('Exception occurred')


    def __xor(self, m):
        pos = 0
        key = self.__key()
        res = ''
        for c in m:
            if pos > len(key)-1:
                pos = 0
            res += chr(ord(key[pos]) ^ ord(c))
            pos += 1
        return res
            
    def get(self, s):
        with open(self.__secrets(), 'r') as f:
            secrets = loads(f.read())
        try:
            return b64decode(self.__xor(secrets[s]).encode()).decode('ASCII')
        except KeyError:
            raise KeyError(f"No secret {s}")

    def put(self, s):
        try:
            with open(self.__secrets(), 'r') as f:
                secrets = loads(f.read())
        except Exception as e:
            secrets = {}
        with open(self.__secrets(), 'w') as f:
            try:
                k, v = s.popitem()
                res = {k:self.__xor(b64encode(v.encode()).decode('ASCII'))}
                secrets.update(res)
                f.write(dumps(secrets))
            except TypeError as e:
                raise TypeError(f'{s} is not dict')
