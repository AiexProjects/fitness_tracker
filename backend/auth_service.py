import hashlib
import os
import binascii
import hmac
import logging

logging.basicConfig(level=logging.INFO, filename='log.log', filemode='w', #keep it write for now
                    format="%(asctime)s - %(levelname)s - %(message)s")

class AuthService:
    @staticmethod
    def hash_password(password):
        salt = os.urandom(16)
        iterations = 1000000

        password_bytes = password.encode('utf-8')
        derived_key = hashlib.pbkdf2_hmac('sha256', password_bytes, salt, iterations, dklen=32)

        hashed_password = binascii.hexlify(derived_key).decode('utf-8')
        salt_hex = binascii.hexlify(salt).decode('utf-8')
    
        return f"pbkdf2_sha256${iterations}${salt_hex}${hashed_password}"
    
    @staticmethod
    def verify_password(password_data, provided_password):
        try:
            data_contents = password_data.split('$')
            if data_contents[0] != "pbkdf2_sha256":
                raise ValueError("Unsupported hash algorithm")
            
            interations = int(data_contents[1])
            salt = binascii.unhexlify(data_contents[2])
            stored_hash = binascii.unhexlify(data_contents[3])

            provided_password_bytes = provided_password.encode('utf-8')
            verification_hash = hashlib.pbkdf2_hmac('sha256', provided_password_bytes, salt, interations, dklen=32)

            return hmac.compare_digest(stored_hash, verification_hash)

        except Exception as e:
            print(f"Error during password verification: {e}")
            logging.error(f"Verification Failiure: {e}")

            return False


#bum code
user_password = input("Password: ")
password_hash = AuthService.hash_password(user_password)
print(password_hash)

verification_password = input("Verify Password: ")
verification = AuthService.verify_password(password_hash, verification_password)

if verification:
    print("Password match! Login successful.")
else:
    print("Incorrect password. Login failed.")