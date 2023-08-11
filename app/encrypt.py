from cryptography.fernet import Fernet


def encrypted(msg,key, en=True):
    f = Fernet(key)
    if en:
        return f.encrypt(bytes(msg, 'utf-8'))
    else:
        return f.decrypt(msg).decode('utf-8')