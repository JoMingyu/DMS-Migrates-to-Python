from hashlib import sha512


def encrypt(s):
    h = sha512()
    h.update(s.encode('utf-8'))
    return h.hexdigest()
