import hashlib
import binascii
import os

def hash_pass(pwd):
    salt = hashlib.sha256(os.urandom(64)).hexdigest().encode('ascii')
    hashedpwd = hashlib.pbkdf2_hmac('sha512', pwd.encode('utf-8'), salt, 1000)
    nhashedpwd = binascii.hexlify(hashedpwd)
    npwd = (salt+nhashedpwd).decode('ascii')
    return npwd

def hash_login(hashed_pwd,pwd):
    salt=hashed_pwd[:64]
    unsalted_pwd = hashed_pwd[64:]
    test = hashlib.pbkdf2_hmac('sha512', pwd.encode('utf-8'), salt.encode('ascii'), 1000)
    hashed_test = binascii.hexlify(test).decode('ascii')
    if hashed_test == unsalted_pwd:
        return True
    return False
