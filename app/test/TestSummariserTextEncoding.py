import os
import django
from django.test import TestCase, Client, RequestFactory, tag
from app.test.test_values import english_test_text, ANSI_encoded_test_text, unicode_encoded_test_text, \
    unicode_big_encoded_test_text

"""
Author: William Blackie
Class for testing the skipthoughts module ability to handel different text encodings.
"""


# Set environment variables to allow running of class individually.
os.environ['DJANGO_SETTINGS_MODULE'] = 'skipthought_django_website.settings'
django.setup()


class TestSummariserTextEncoding(TestCase):
    """
    Test methods for the text encoding of the Skip-Thought summariser
    """

    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()

    @tag('slow', 'core')
    def test_summarise_text_file_encoding_UTF8(self):
        """
        Method for testing the correct response for a valid UTF-8 encoded file.
        """
        with open(english_test_text, "rb") as text:
            form_data = \
                {"url": "", "compression_rate": float(0.7), "remove_lists": True, "file": text}
            response = self.client.post('/summariser/', form_data, follow=True, format='multipart')
        self.assertEqual(response.status_code, 200,
                         "Correct status code: 200 actual response: %s" % response.status_code)
        self.assertTemplateUsed('summary_output.html')

    @tag('fast', 'core')
    def test_summarise_text_file_encoding_ANSI(self):
        """
        Method for testing the correct response for a invalid ANSI encoded file.
        """
        with open(ANSI_encoded_test_text, "rb") as text:
            form_data = \
                {"url": "", "compression_rate": float(0.7), "remove_lists": True, "file": text}
            response = self.client.post('/summariser/', form_data, follow=True, format='multipart')
        self.assertEqual(response.status_code, 200,
                         "Correct status code: 200 actual response: %s" % response.status_code)
        self.assertTemplateUsed('input_error.html')

    @tag('fast', 'core')
    def test_summarise_text_file_encoding_unicode(self):
        """
        Method for testing the correct response for a invalid Unicode encoded file.
        """
        with open(unicode_encoded_test_text, "rb") as text:
            form_data = \
                {"url": "", "compression_rate": float(0.7), "remove_lists": True, "file": text}
            response = self.client.post('/summariser/', form_data, follow=True, format='multipart')
        self.assertEqual(response.status_code, 200,
                         "Correct status code: 200 actual response: %s" % response.status_code)
        self.assertTemplateUsed('input_error.html')

    @tag('fast', 'core')
    def test_summarise_text_file_encoding_unicode_big(self):
        """
        Method for testing the correct response for a invalid Unicode big endian encoded file.
        """
        with open(unicode_big_encoded_test_text, "rb") as text:
            form_data = \
                {"url": "", "compression_rate": float(0.7), "remove_lists": True, "file": text}
            response = self.client.post('/summariser/', form_data, follow=True, format='multipart')
        self.assertEqual(response.status_code, 200,
                         "Correct status code: 200 actual response: %s" % response.status_code)
        self.assertTemplateUsed('input_error.html')

