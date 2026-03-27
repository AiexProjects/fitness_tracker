import hashlib
import os
import binascii
import hmac
import logging
import uuid

logging.basicConfig(level=logging.INFO, filename='log.log', filemode='a',
                    format="%(asctime)s - %(filename)s - %(levelname)s - %(message)s")

class AuthService: #might change to argon2id (hybrid) or argon2i (frontend password hashing)
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
    
    @staticmethod
    def create_new_user_id():
        try:
            unique_user_id = str(uuid.uuid4())

            return unique_user_id
        except Exception as e:
            logging.error(f"User Creation Failiure: {e}")




"""
What I've learnt so far,
- use of salt and iteration when hashing sensitive data to add uniquness and slow down any bruteforcing.
- different hashing algorithms, deciding to use pbkdf2-sha256, as it showcase understanding of salt and iterations,
  also using sha256 instead of sha512 as sha512 is more targeted towards 64-bit device and we want to use this for mobile devices
- different ways our auth service can be attacked, what algorithm to defend against it(pbkdf2-sha256 is cpu focused and susceptible to gpu based attack).
- use of os.urandom() to generate a random 16byte salt, learning difference between prng, csprng, trng
  basic understanding of how csprng is generated (use of entropy pool - what entropy pool is made up of)
- basic error logging for better error analysis
- learned that using logging.exception() is bad for our case as it provides the user with too much info about the error,
  which can be malliciously used.
- generating a fixed length hash to prevent timing attack,
  use of cryptography secure comparison function rathar than simple == when comparing hash
"""