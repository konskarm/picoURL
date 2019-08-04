from django.test import TestCase

from utils.config import CONFIG
from utils.hasher import URLHasher


class URLHasherTests(TestCase):
    """
    This class is used to test the URLHasher class.
    """

    def setUp(self):
        """
        Define the original url and a random short code.
        """
        self.original_url = "https://ultimaker.com/en/knowledge/33-reducing-costs-and-improving-efficiency-with-the-ultimaker-s5"
        self.url_hasher = URLHasher()
        self.short_code = self.url_hasher.hash(self.original_url)

    def test_can_create_hash(self):
        self.assertEqual(len(self.short_code), CONFIG.SHORT_CODE_SIZE)
        self.assertEqual(self.short_code, 'WkJKycfjnr')

    def test_hashing_same_url(self):
        url_hasher2 = URLHasher()
        short_code2 = url_hasher2.hash(self.original_url)
        self.assertEqual(self.short_code, short_code2)

    def test_rehash_same_url(self):
        url_hasher2 = URLHasher()
        short_code2 = url_hasher2.hash(self.original_url)
        short_code2_rehashed = url_hasher2.rehash()

        short_code1_rehashed = self.url_hasher.rehash()
        # There might be a slight chance that this test will fail because random generated the same number
        # accidentally. It's possible to avoid this using a fixed seed for random.
        self.assertNotEqual(short_code2_rehashed, short_code1_rehashed)

    def test_can_rehash(self):
        short_code2 = self.url_hasher.rehash()
        self.assertNotEqual(self.short_code, short_code2)
