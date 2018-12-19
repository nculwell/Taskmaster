#!/usr/bin/python3
# vim: et ts=8 sts=4 sw=4

import hashlib, binascii

def HashPassword(password, passwordEncoding='utf8'):
    pwdEncoded = password.encode(passwordEncoding)
    h = hashlib.sha256(pwdEncoded)
    h.update(pwdEncoded)
    pwdSha256 = h.digest()
    return pwdSha256

def BinToHex(binary):
    hex = binascii.b2a_hex(binary)
    return hex.decode('ascii')

def HexToBin(hex):
    binary = binascii.a2b_hex(hex)
    return binary

