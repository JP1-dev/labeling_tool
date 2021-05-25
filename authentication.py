from hashlib import sha256


class Authenticator():
    def __init__(self, secret_key):
        self.secret_key= secret_key

    def sign(self, id):
        return sha256((id + self.secret_key).encode()).hexdigest()

    def validate(self, id, key):
        return sha256((id + self.secret_key).encode()).hexdigest() == key

