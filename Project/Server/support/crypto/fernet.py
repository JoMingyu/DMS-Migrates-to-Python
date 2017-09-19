from cryptography.fernet import Fernet

key = b'wWxosi44Q48_aZ88q9kz=SxSa_V'
cipher_suite = Fernet(key)


def encrypt(s):
    return cipher_suite.encrypt(s.encode('utf-8')).decode('utf-8')


def decrypt(s):
    return cipher_suite.decrypt(s.encode('utf-8')).decode('utf-8')
