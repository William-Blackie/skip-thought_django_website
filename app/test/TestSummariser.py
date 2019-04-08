import os
import django
from django.test import TestCase, RequestFactory, tag, Client
from app.test.test_values import english_test_text, spanish_test_text, german_test_text, english_test_url_bbc, \
    english_test_url_new_york_times, english_test_url_thegaurdian, spanish_test_url, german_test_url

"""
Author: William Blackie
Class for testing the Skip-Thought Summariser.
"""

# Set environment variables to allow running of class individually.
os.environ['DJANGO_SETTINGS_MODULE'] = 'skipthought_django_website.settings'
django.setup()


class TestSummariser(TestCase):
    """
    Test methods for the Skip-Thought summariser
    """
    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()

    @tag('slow', 'core')
    def test_summarise_text_file_english(self):
        """
        Method for testing the correct response for an english.txt file.
        """
        with open(english_test_text, "rb") as text:
            form_data = \
                {"url": "", "compression_rate": float(0.3), "remove_lists": True, "file": text}
            response = self.client.post('/summariser/', form_data, follow=True, format='multipart')
        self.assertEqual(response.status_code, 200,
                         "Correct status code: 200 actual response: %s" % response.status_code)
        self.assertTemplateUsed('summary_output.html')

    @tag('fast', 'core')
    def test_summarise_text_file_spanish(self):
        """
        Method for testing the correct response for an spanish.txt file.
        """
        with open(spanish_test_text, "rb") as text:
            form_data = \
                {"url": "", "compression_rate": float(0.3), "remove_lists": True,
                 "file": text}
            response = self.client.post('/summariser/', form_data, follow=True, format='multipart')
        self.assertEqual(response.status_code, 200,
                         "Correct status code: 200 actual response: %s" % response.status_code)
        self.assertTemplateUsed('input_error.html')

    @tag('fast', 'core')
    def test_summarise_text_file_german(self):
        """
        Method for testing the correct response for an german.txt file.
        """
        with open(german_test_text, "rb") as text:
            form_data = \
                {"url": "", "compression_rate": 0.3, "remove_lists": True,
                 "file": text}
            response = self.client.post('/summariser/', form_data, follow=True, format='multipart')
        self.assertEqual(response.status_code, 200, "Correct status code: 200 actual response: %s" % response.status_code)
        self.assertTemplateUsed('input_error.html')

    @tag('slow', 'core')
    def test_summarise_url_english(self):
        """
        Method for testing the correct response for an english.txt file.
        """
        form_data = \
            {"url": english_test_url_bbc,
             "compression_rate": float(0.3),
             "remove_lists": True,
             "file": None}

        response = self.client.post('/summariser/', form_data, follow=True, format='multipart')
        self.assertEqual(response.status_code, 200,
                         "Correct status code: 200 actual response: %s" % response.status_code)
        self.assertTemplateUsed('summary_output.html')

    @tag('slow', 'core')
    def test_summarise_url_new_york_times(self):
        """
        Method for testing the correct response for an english.txt file.
        """
        form_data = \
            {"url": english_test_url_new_york_times,
             "compression_rate": float(0.3),
             "remove_lists": True,
             "file": None}

        response = self.client.post('/summariser/', form_data, follow=True, format='multipart')
        self.assertEqual(response.status_code, 200,
                         "Correct status code: 200 actual response: %s" % response.status_code)
        self.assertTemplateUsed('summary_output.html')

    @tag('slow', 'core')
    def test_summarise_url_the_guardian(self):
        """
        Method for testing the correct response for an english.txt file.
        """
        form_data = \
            {"url": english_test_url_thegaurdian,
             "compression_rate": float(0.3),
             "remove_lists": True,
             "file": None}

        response = self.client.post('/summariser/', form_data, follow=True, format='multipart')
        self.assertEqual(response.status_code, 200,
                         "Correct status code: 200 actual response: %s" % response.status_code)
        self.assertTemplateUsed('summary_output.html')

    @tag('fast', 'core')
    def test_summarise_url_spanish(self):
        """
        Method for testing the correct response for an spanish.txt file.
        """
        form_data = \
            {"url": spanish_test_url,
             "compression_rate": 0.3,
             "remove_lists": True,
             "file": None}

        response = self.client.post('/summariser/', form_data, follow=True, format='multipart')
        self.assertEqual(response.status_code, 200,
                         "Correct status code: 200 actual response: %s" % response.status_code)
        self.assertTemplateUsed('input_error.html')

    @tag('fast', 'core')
    def test_summarise_url_german(self):
        """
        Method for testing the correct response for an german.txt file.
        """
        form_data = \
            {"url": german_test_url,
             "compression_rate": 0.3,
             "remove_lists": True,
            "file": None}
        response = self.client.post('/summariser/', form_data, follow=True, format='multipart')
        self.assertEqual(response.status_code, 200, "Correct status code: 200 actual response: %s" % response.status_code)
        self.assertTemplateUsed('input_error.html')


