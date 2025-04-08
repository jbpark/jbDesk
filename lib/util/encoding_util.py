from cryptography.fernet import Fernet

from lib.models.constants.const_key import LDAP_KEY


def decrypt_cipher_text(ciphered_text):
    cipher_suite = Fernet(LDAP_KEY)
    try:
        result = str((cipher_suite.decrypt(ciphered_text.encode())), 'utf-8')
    except Exception as e:
        result = None
        print(f"An error occurred: {e}")

    return result


def encrypt_cipher_text(text):
    cipher_suite = Fernet(LDAP_KEY)
    try:
        result = str(cipher_suite.encrypt(text.encode()).decode())
    except Exception as e:
        result = None
        print(f"An error occurred: {e}")

    return result
