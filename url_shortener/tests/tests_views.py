from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from url_shortener.models import URLMapping


class CreateURLMappingViewTestCase(TestCase):
    """
    Tests the CreateURLMappingView.
    """

    def setUp(self):
        """
        Define the test client and other test variables.
        """
        self.client = APIClient()
        self.original_url = "https://ultimaker.com/en/knowledge/33-reducing-costs-and-improving-efficiency-with-the-ultimaker-s5"
        self.input_data = {'original_url': self.original_url}

        self.post_response = self.client.post(
            reverse('create'),
            self.input_data,
            format='json'
        )

    def test_can_create_a_url_mapping(self):
        self.assertEqual(self.post_response.status_code, status.HTTP_201_CREATED)
        obj = URLMapping.objects.filter(original_url=self.original_url)
        self.assertTrue(obj.exists())
        self.assertEqual(obj.count(), 1)
        self.assertEqual(obj.first().original_url, self.original_url)

    def test_duplicate_url_with_different_short_codes(self):
        duplicate_url_response = self.client.post(
            reverse('create'),
            self.input_data,
            format='json'
        )
        objects = URLMapping.objects.filter(original_url=self.original_url)
        self.assertEqual(objects.count(), 2)
        self.assertNotEqual(objects.first().short_code, objects.last().short_code)

    def test_rejects_wrong_url(self):
        self.post_response = self.client.post(
            reverse('create'),
            {"original_url": "random string"},
            format='json'
        )
        self.assertEqual(self.post_response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_response_data_contains_only_short_code(self):
        """
        Tests whether the output json contains only the 'short_code' field.
        """
        self.assertEqual(list(self.post_response.data.keys()), ['short_code'])


class RedirectViewTestCase(TestCase):
    """
    Tests the view that redirects to the original URL on a GET request.
    """

    def setUp(self):
        self.client = APIClient()
        self.original_url = "https://ultimaker.com/en/knowledge/33-reducing-costs-and-improving-efficiency-with-the-ultimaker-s5"
        self.input_data = {'original_url': self.original_url}

        self.post_response = self.client.post(
            reverse('create'),
            self.input_data,
            format='json'
        )

    def test_redirect_view_redirects_to_original_url(self):
        """
        Makes sure that the redirect view returns an 302 response and then redirects us to the original url.
        :return:
        """
        get_response = self.client.get(
            reverse('redirect', kwargs={"short_code": self.post_response.data['short_code']})
        )
        self.assertEqual(get_response.status_code, status.HTTP_302_FOUND)
        self.assertRedirects(get_response, self.original_url, fetch_redirect_response=False)

    def test_redirects_increase_times_used(self):
        """
        Tests whether the GET requests increase the times_used counter when redirecting.
        """
        for i in range(10):
            self.client.get(
                reverse('redirect', kwargs={"short_code": self.post_response.data['short_code']})
            )
        obj = URLMapping.objects.filter(short_code=self.post_response.data['short_code']).first()
        self.assertEqual(obj.times_used, 10)

    def test_returns_404_on_non_existing_short_code(self):
        """
        Tests whether we get a 404 error when trying to access a non-existing short_code

        NOTE: Hopefully, the hashing of the self.original_url doesn't actually result to the word "random"!
        """
        bad_get_response = self.client.get(
            reverse('redirect', kwargs={"short_code": 'random'})
        )
        self.assertEqual(bad_get_response.status_code, status.HTTP_404_NOT_FOUND)
