import ecdsa
import os

class DecentralizedIdentityCreation:
    def __init__(self):
        # Generate key pair during object instantiation
        self.private_key, self.public_key = self.generate_key_pair()
        # Initialize the RegisterAcademic instance with the public key
        self.register_academic = RegisterAcademic(self.public_key)
        # Create a storage facility for the creation of the public and private key
        self.key_storage = {}

    def get_public_key(self, private_key):
        # Convert the private key back to a string before retrieving the public key
        private_key_str = private_key.to_string().hex()
        return self.key_storage.get(private_key_str)

    def generate_key_pair(self):
        # Generate a private key
        private_key = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1, entropy=os.urandom)

        # Derive the corresponding public key
        public_key = private_key.get_verifying_key()
        self.key_storage[private_key.to_string().hex()] = public_key.to_string().hex()

        # Return the private key and public key
        return private_key, public_key

    def get_keys(self):
        # Return the private and public keys
        return self.private_key, self.public_key
    

class RegisterAcademic:
    def __init__(self, public_key):
        self.user_public_key = public_key
        self.users_data = {}

    def add_gmail(self, gmail_hash):
        self.users_data[self.user_public_key] = {}  # A hash map is registered for the public key
        self.users_data[self.user_public_key]["Gmail"] = gmail_hash
        return "Gmail has been added"

    def access_gmail(self, public_key):
        return self.users_data[public_key]["Gmail"]

    def change_email(self, private_key, changed_gmail_hash):
        public_key = private_key.get_verifying_key().to_string().hex()
        print(f'public key of the private key is: {public_key}')
        if public_key in self.users_data:
            self.users_data[public_key]["Gmail"] = changed_gmail_hash
        return "Gmail has been changed"
    

class Login:
    def __init__(self, private_key):
        self.user_private_key = private_key
        public_key = DecentralizedIdentityCreation().get_public_key(private_key)
        print(f'the public key is: {public_key}')
        Register_data = RegisterAcademic(public_key)
        email_hash = Register_data.access_gmail(public_key)
        if email_hash:
            self.login_successful = True
        else:
            self.login_successful = False

import hashlib
# Step 1: Generate Decentralized Identity
identity_creator = DecentralizedIdentityCreation()
private_key, public_key = identity_creator.get_keys()
print(f'private key is: {private_key.to_string().hex()} and public key is: {public_key.to_string().hex()}')
# Step 2: Register an Email
email = "test@example.com"
hashed_email = hashlib.sha256(email.encode()).hexdigest()
print(f'hashed email value is: {hashed_email}')
register_academic = identity_creator.register_academic
print(register_academic.add_gmail(hashed_email))
# Step 3: Access Email Data
retrieved_email = register_academic.access_gmail(public_key.to_string().hex())
print("Retrieved Email:", retrieved_email)
# Step 4: Change Email (Optional)
new_email = "new_test@example.com"
hashed_new_email = hashlib.sha256(new_email.encode()).hexdigest()
print(register_academic.change_email(private_key, hashed_new_email))
# Step 5: Login
login_attempt = Login(private_key)
if login_attempt.login_successful:
    print("Login Successful")
else:
    print("Login Failed")
