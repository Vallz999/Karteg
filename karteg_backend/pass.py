import bcrypt

print(
    bcrypt.hashpw(
        b"admin12345",
        bcrypt.gensalt()
    ).decode()
)