import base64
import hashlib
import random

from utils.config import CONFIG


class URLHasher():
    """
    Class that handles the hashing and truncating.
    """
    def __init__(self):
        self.hasher = hashlib.sha1()

    def hash(self, input:str , size: int=CONFIG.SHORT_CODE_SIZE):
        """

        :param input:
        :param size:
        :return: short_code
        """
        self.hasher.update(input.encode('utf-8'))
        b64 = base64.urlsafe_b64encode(self.hasher.digest())
        hashed_link = b64.decode()
        short_code = hashed_link[:size]
        return short_code

    def rehash(self, size: int=CONFIG.SHORT_CODE_SIZE):
        random_str = str(random.random())
        return self.hash(random_str, size=size)