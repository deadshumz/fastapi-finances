from passlib.context import CryptContext

myctx = CryptContext(schemes=["sha256_crypt", "md5_crypt", "des_crypt"])


def hash_password(password: str) -> str:
    return myctx.hash(password)
