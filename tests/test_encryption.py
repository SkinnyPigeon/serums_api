from components.encryption.encryption import encrypt_data_with_new_key, \
                                             encrypt_key
from cryptography.hazmat.backends.openssl.rsa import _RSAPublicKey
import binascii

public_key = "-----BEGIN PUBLIC KEY-----\n"\
             "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCB"\
             "iQKBgQCLCWYFVX0YmP4Hezn7fOdTFiuO\n"\
             "41c8ZLLpN0jCAZjLPCi6ZFN1nhaXn9Hu"\
             "CJFIYimPDC04u1VJclD5GfVE6zuDRUcq\n"\
             "tVDQP/Qw88WKpDY4e2zjIddIC0Qs9uE1"\
             "ErX7ae+yQE8vXf0OTrBZQRyCH7DtM4/e\n"\
             "pAJ84ck6ySK3CIwF0QIDAQAB\n"\
             "-----END PUBLIC KEY-----"

fernet_key = b'uCbic5HN4gpy8YK0Bn4EOdi2CupvlSVu0S9Z-oJrSEI='


def test_can_encrypt_data():
    result = encrypt_data_with_new_key({'test': 'data'}, public_key)
    assert type(result[0]) == str
    assert {'test': 'data'} not in result


def test_can_encrypt_key():
    keys = encrypt_data_with_new_key({'test': 'data'}, public_key)
    key = encrypt_key(fernet_key, public_key=keys[2])
    assert type(key) == str
    assert key != fernet_key
