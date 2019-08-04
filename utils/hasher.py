import base64
import hashlib
import random

from utils.config import CONFIG


class URLHasher():
    """
    Class that handles the hashing and truncating. Acts as a facade to the hashing process.
    """

    def __init__(self):
        self.hasher = hashlib.sha1()

    def hash(self, input_string: str, size: int = CONFIG.SHORT_CODE_SIZE):
        """
        Function that hashes an input string using the sha1 algorithm.
        When it is called again with a new input string, it appends it at the end of the old one
        and reruns the hash.
        :param input_string: string to be shorted
        :param size: the size that the hash will be truncated to.
        :return: hashed version of the input string, truncated.
        """
        self.hasher.update(input_string.encode('utf-8'))
        b64 = base64.urlsafe_b64encode(self.hasher.digest())
        hashed_link = b64.decode()
        return hashed_link[:size]

    def rehash(self, size: int = CONFIG.SHORT_CODE_SIZE):
        """
        It re-genenerates a hash code for the previous hashed url.
        This is done by appending a random number to the previous input string and rehashing it.
        :param size: The size that the new hash will be truncated to.
        :return: The new short code
        """
        random_str = str(random.random())
        return self.hash(random_str, size=size)
