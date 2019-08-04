from django.test import TestCase

from url_shortener.models import URLMapping


class URLMappingModelTestCase(TestCase):
    """
    This class is used to test the URLMapping model.
    """

    def setUp(self):
        """
        Define the original url and a random short code.
        """
        self.original_url = "https://ultimaker.com/en/knowledge/33-reducing-costs-and-improving-efficiency-with-the-ultimaker-s5"
        self.short_code = "asv12Hb91c"
        self.url_mapping = URLMapping(short_code=self.short_code, original_url=self.original_url)

    def test_model_can_create_a_URLMapping(self):
        """
        TODO we can test the model, but its functionality is already tested by Django. Does it make sense to keep it?
        This is a sample of testing the model, but Django is already testing these functionalities
        As my code does not have any functions inside the model, we do not really need to test anything.
        """
        old_count = URLMapping.objects.count()
        self.url_mapping.save()
        new_count = URLMapping.objects.count()
        self.assertNotEqual(old_count, new_count)
