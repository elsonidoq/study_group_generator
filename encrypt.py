from cryptography.fernet import Fernet

def encrypt_file(filename):   
    # read file
    with open(filename, 'rb') as f:
        data = f.read()   
    # encrypt
    key = Fernet.generate_key()
    fernet = Fernet(key)
    data_enc = fernet.encrypt(data)
    # save encrypted
    with open(str(filename)+'.enc', 'wb') as f:
        f.write(data_enc)
    with open(str(filename)+'.key', 'wb') as f:
        f.write(key)


def load_decrypted(fname, key):
    with open(fname, 'rb') as f:
        return Fernet(key).decrypt(f.read())


