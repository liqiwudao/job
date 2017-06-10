#-*- coding:utf-8 -*-
import hashlib
import hmac
import base64
from random import choice
import string
from bson import ObjectId

from flask import json


_chars = string.printable[:87] + '_' + string.printable[90:95]


def gen_random_str(length=6, chars=_chars):
    return ''.join(choice(chars) for i in range(length))


def gen_weixin_auth_code():
    return gen_random_str(2, 'ABCEFGHJKMNPQRSTUVWXYZ') + gen_random_str(4, string.digits)


def gen_random_js_str(length=12):
    chars = string.ascii_letters + string.digits + '_=-'
    return gen_random_str(length, chars)


def sign_app_auth_message(secret_key, encoded_message):
    message_signed = hmac.new(str(secret_key), encoded_message, hashlib.sha1)
    return base64.b64encode(message_signed.digest())


def gen_app_auth_header(app_id, secret_key, message):
    encoded_message = base64.b64encode(json.dumps(message))
    signed_message = sign_app_auth_message(secret_key, encoded_message)
    return "%s:%s:%s" % (app_id, signed_message, encoded_message)


def decode_app_auth_message(secret_key, message_digest, encoded_message):
    if message_digest != sign_app_auth_message(secret_key, encoded_message):
        return None
    return json.loads(base64.b64decode(encoded_message))


def make_sign_token(secret_key, plain_message, salt):
    message_signed = hmac.new(str(secret_key), plain_message, hashlib.sha256).hexdigest()
    return hmac.new(salt, message_signed, hashlib.md5).hexdigest()


def generate_random_hmac_key():
    s = str(ObjectId())
    k = gen_random_str()
    key = hmac.HMAC(k, s).hexdigest()
    return key
