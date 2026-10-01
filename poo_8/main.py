import seguridad

salt = seguridad.generar_salt()
print("SALT:", salt)

pwd_hashed = seguridad.hashear_password("hola123", salt)
print("Password hasheada:", pwd_hashed)

is_valid = seguridad.verificar_password("hola123", salt, pwd_hashed)
if is_valid:
    print("Ud. puede ingresar.")
else:
    print("Sus credenciales no son validas.")