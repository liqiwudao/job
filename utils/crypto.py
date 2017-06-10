# -*- coding:utf-8 -*-
__author__ = 'night'

from Crypto.Cipher import AES
from Crypto import Random
from Crypto.Hash import MD5
import base64
import os
import hmac
import hashlib
import binascii

BS = AES.block_size
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
unpad = lambda s: s[0:-ord(s[-1])]


def random_key():
    key = os.urandom(32)
    return binascii.b2a_hex(key)


def _openssl_kdf(req, secret, salt):
    prev = ''
    while req > 0:
        prev = MD5.new('{0}{1}{2}'.format(prev, secret, salt)).digest()
        req -= 16
        yield prev


def openssl_evp_byte2key(password, salt, key_len, iv_len):
    """
    Derive the key and the IV from the given password and salt.

    see OpenSSL man:
    https://www.openssl.org/docs/crypto/EVP_BytesToKey.html
    """
    # from hashlib import md5
    # dtot = md5(password + salt).digest()
    # d = [ dtot ]
    # while len(dtot)<(iv_len+key_len):
    #     d.append( md5(d[-1] + password + salt).digest() )
    #     dtot += d[-1]
    # return dtot[:key_len], dtot[key_len:key_len+iv_len]
    dtot = MD5.new('{0}{1}'.format(password, salt)).digest()
    d = [dtot]
    while len(dtot) < (iv_len + key_len):
        d.append(MD5.new('{0}{1}{2}'.format(d[-1], password, salt)).digest())
        dtot += d[-1]
    return dtot[:key_len], dtot[key_len:key_len + iv_len]


def openssl_aes_decrypt(encoded_text, password_phase):
    """
    Decrypt an openssl-compatible 256-bit AES cipher text
    :param encoded_text:
    :param password_phase:
    :return:
    """
    encrypted = base64.b64decode(encoded_text)
    salt = encrypted[8:16]
    data = encrypted[16:]
    # mat = ''.join([x for x in _openssl_kdf(32+16, secret, salt)])
    # key = mat[0:32]
    # iv = mat[32:48]
    key, iv = openssl_evp_byte2key(password_phase, salt, 32, 16)
    dec = AES.new(key, AES.MODE_CBC, iv)
    plain_text = dec.decrypt(data)
    return unpad(plain_text)


def openssl_aes_encrypt(plain_text, password_phase):
    salt = Random.new().read(8)
    key, iv = openssl_evp_byte2key(password_phase, salt, 32, 16)
    enc = AES.new(key, AES.MODE_CBC, iv)
    plain_text = pad(plain_text)
    return base64.b64encode(salt) + base64.b64encode(enc.encrypt(plain_text))


def encrypt_urlsafe_token(data, password_phase):
    salt = os.urandom(8)
    key, iv = openssl_evp_byte2key(password_phase, salt, 32, 16)
    enc = AES.new(key, AES.MODE_CBC, iv)
    data = pad(data)
    cipher_text = base64.urlsafe_b64encode(salt + enc.encrypt(data))
    h = hmac.HMAC(password_phase, cipher_text).hexdigest()
    return cipher_text + h


def decrypt_urlsafe_token(token, password_phase):
    if isinstance(token, unicode):
        token = token.encode('utf8', 'replace')
    sign = token[-32:]
    encrypt_data = token[:-32]
    if hmac.HMAC(password_phase, encrypt_data).hexdigest() != sign:
        return
    encrypt_data = base64.urlsafe_b64decode(encrypt_data)
    salt = encrypt_data[:8]
    cipher_text = encrypt_data[8:]
    key, iv = openssl_evp_byte2key(password_phase, salt, 32, 16)
    enc = AES.new(key, AES.MODE_CBC, iv)
    return unpad(enc.decrypt(cipher_text))
