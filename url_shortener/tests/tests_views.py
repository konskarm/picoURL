from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient


class CreateURLMappingViewTestCase(TestCase):
    """
    Tests the CreateURLMappingView.
    """

    @classmethod
    def setUpClass(cls):
        # The APIClient and the original url are used by all the tests in this class.
        cls.client = APIClient()
        cls.original_url = "https://ultimaker.com/en/knowledge/33-reducing-costs-and-improving-efficiency-with-the-ultimaker-s5"

    def setUp(self):
        """
        Define the test client and other test variables.
        """
        self.input_data = {'original_url': self.original_url}
        self.post_response = self.client.post(
            reverse('create'),
            self.input_data,
            format='json'
        )

    def test_can_create_a_url_mapping(self):
        self.assertEqual(self.post_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.post_response.data['short_code'], 'WkJKycfjnr')

    def test_duplicate_url_with_different_short_codes(self):
        duplicate_url_response = self.client.post(
            reverse('create'),
            self.input_data,
            format='json'
        )
        self.assertEqual(duplicate_url_response.status_code, status.HTTP_201_CREATED)
        self.assertNotEqual(self.post_response.data['short_code'], duplicate_url_response.data['short_code'])

    def test_rejects_wrong_url(self):
        # Even though the code validates whether the url is correctly formatted, the exception comes
        # from Django itself.
        self.post_response = self.client.post(
            reverse('create'),
            {"original_url": "bad formatted url"},
            format='json'
        )
        self.assertEqual(self.post_response.status_code, status.HTTP_400_BAD_REQUEST)

    @classmethod
    def tearDownClass(cls):
        pass


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
        stats_response = self.client.get(
            reverse('short-code-stats', kwargs={"short_code": self.post_response.data['short_code']}))
        self.assertEqual(stats_response.data['times_used'], 10)

    def test_returns_404_on_non_existing_short_code(self):
        """
        Tests whether we get a 404 error when trying to access a non-existing short_code

        NOTE: Hopefully, the hashing of the self.original_url doesn't actually result to the word "random"!
        """
        bad_get_response = self.client.get(
            reverse('redirect', kwargs={"short_code": 'random'})
        )
        self.assertEqual(bad_get_response.status_code, status.HTTP_404_NOT_FOUND)


class UsageDetailsViewTestCase(TestCase):
    """
    Tests the view that returns the usage statistics of a short_code.
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

    def test_details_view_returns_correct_data(self):
        """
        Tests whether the response contains the correct data.
        """
        get_response = self.client.get(
            reverse('short-code-stats', kwargs={"short_code": self.post_response.data['short_code']})
        )
        self.assertEqual(get_response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(get_response.data), 3)
        self.assertEqual(['original_url', 'creation_date', 'times_used'], list(get_response.data.keys()))
        self.assertEqual(get_response.data['original_url'], self.original_url)
        self.assertEqual(get_response.data['times_used'], 0)

    def test_details_view_returns_404_on_wrong_short_code(self):
        """
        Tests whether the response status is 404 if the given short code does not exist in the database.
        """
        get_response = self.client.get(
            reverse('short-code-stats', kwargs={"short_code": "random"})
        )
        self.assertEqual(get_response.status_code, status.HTTP_404_NOT_FOUND)
