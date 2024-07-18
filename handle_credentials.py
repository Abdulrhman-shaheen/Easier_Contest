import os

from cryptography.fernet import Fernet


class credentials:
    def __init__(self, user=None, password=None) -> None:
        self.user = user
        self.password = password
        self.key = None

    def write_key(self):
        key = Fernet.generate_key()
        with open("secret.key", "wb") as key_file:
            key_file.write(key)
            return key

    def load_key(self):
        with open("secret.key", "rb") as key_file:
            key = key_file.read()
            return key

    def encrypt(self, message):
        try:
            key = self.load_key()
        except FileNotFoundError:
            key = self.write_key()

        encrypted = Fernet(key).encrypt(message.encode())
        return encrypted

    def decrypt(self, message):
        return Fernet(self.load_key()).decrypt(message)

    def save(self):
        encrypted_user = self.encrypt(self.user)
        encrypted_password = self.encrypt(self.password)
        with open("credential.txt", "wb") as f:
            f.write(encrypted_user + b"\n" + encrypted_password)

    def load(self):
        try:
            with open("credential.txt", "rb") as f:
                encrypted_u, encrypted_p = f.read().split(b"\n")

                decrypted_user = self.decrypt(encrypted_u).decode()
                decrypted_password = self.decrypt(encrypted_p).decode()

            return (decrypted_user, decrypted_password)
        except FileNotFoundError:
            print(
                "Look like you are new here! Please run  'python main.py -c 1' to first save your log in credentials. Only ONCE!"
            )
            exit()


# obj = credentials(user_ex, pass_ex)
# encrypted = obk.save()
# decrypted = obj.load()
# print(decrypted)
