from cryptography.fernet import Fernet

# we will be encryting the below string.
message = "School"

# generate a key for encryptio and decryption
# You can use fernet to generate
# the key or use random key generator
# here I'm using fernet to generate key

key = b'RwdEWFPygOggOdXRkNSKGM8Wm58QT6ZIpZ34oauwkSE='
print("key",key)
# Instance the Fernet class with the key
enc1 = b'gAAAAABhx6uFK2uWbJoJqkYq539ViF8Kf9cB7EG3W5KthB1AM2GngmqvowA19r3tlLsx6hRe1nJ6h-0zrMfClOEY78aEDb2E3Q=='
enc2 = 'gAAAAABhx6qNt4eYkLmsNoEWiH9JWkKlJefGNmp44ZDoH9HyPmTt1XO0Y1AUb2XlSFqJ5vVAcUnVjnBm8zcaf79Shzo0KlhECw=='
fernet = Fernet(key)

print(fernet.decrypt(enc1).decode())
print(fernet.decrypt(enc2).decode())
# # then use the Fernet class instance
# # to encrypt the string string must must
# # be encoded to byte string before encryption
# encMessage = fernet.encrypt(message.encode())

# print("original string: ", message)
# print("encrypted string: ", encMessage)

# # decrypt the encrypted string with the
# # Fernet instance of the key,
# # that was used for encrypting the string
# # encoded byte string is returned by decrypt method,
# # so decode it to string with decode methods
# decMessage = fernet.decrypt(encMessage).decode()

# print("decrypted string: ", decMessage)
