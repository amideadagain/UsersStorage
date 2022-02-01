from passlib.context import CryptContext

password_cxt = CryptContext(schemes=["bcrypt"], deprecated="auto")


def bcrypt(password: str):
    return password_cxt.hash(password)
