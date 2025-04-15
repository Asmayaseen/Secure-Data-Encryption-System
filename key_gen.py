from cryptography.fernet import Fernet

key = Fernet.generate_key()
print("Generated SECRET_KEY:", key.decode())
