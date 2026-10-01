import hashlib
import hmac
import os

ITERACIONES = 600_000 # costo del hash: es lento para quien intente adivinar

def generar_salt() -> bytes:
    # Valor aleatorio por usuario
    return os.urandom(16)

def hashear_password(password: str, sal: bytes) -> bytes:
    return hashlib.pbkdf2_hmac(
        "sha-256", password.encode('utf-8'), sal, ITERACIONES
    )


def verificar_password(password: str, sal: bytes, hash_guardado: bytes) -> bool:
    password_ingresada_hashed = hashear_password(password, sal)
    return hmac.compare_digest(password_ingresada_hashed, hash_guardado)
