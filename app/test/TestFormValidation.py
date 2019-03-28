from django.test import Client, tag, RequestFactory, TestCase
from app.test.test_values import english_test_url_bbc, large_english_test_text, invalid_file_type_text
import django
import os

"""
Author: William Blackie
Class for testing the argument validation of app.PostForm 
"""

# Set environment variables to allow running of class individually.
os.environ['DJANGO_SETTINGS_MODULE'] = 'skipthought_django_website.settings'
django.setup()


class TestFormValidation(TestCase):
    """
    Testing methods of the validation for app.forms
    """
    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()

    @tag('fast', 'core')
    def test_form_invalid_url(self):
        """
        Testing the correct response to an invalid URL argument.
        """
        form_data = \
                {"url": "foobar", "compression_rate": float(0.7), "remove_lists": True, "file": None}
        response = self.client.post('/summariser/', form_data, follow=True, format='multipart')
        self.assertEqual(response.status_code, 200,
                         "Correct status code: 200 actual response: %s" % response.status_code)
        self.assertTemplateUsed('input_error.html')

    @tag('fast', 'core')
    def test_form_invalid_upper_compression(self):
        """
        Testing the correct response to an invalid argument; compression_rate of the upper validator.
        """

        form_data = \
            {"url": english_test_url_bbc, "compression_rate": float(1.1), "remove_lists": True, "file": None}
        response = self.client.post('/summariser/', form_data, follow=True, format='multipart')
        self.assertEqual(response.status_code, 200,
                         "Correct status code: 200 actual response: %s" % response.status_code)
        self.assertTemplateUsed('input_error.html')

    @tag('fast', 'core')
    def test_form_invalid_lower_compression(self):
        """
        Testing the correct response to an invalid argument; compression_rate of the lower validator.
        """

        form_data = \
            {"url": english_test_url_bbc, "compression_rate": float(-1.0), "remove_lists": True, "file": None}
        response = self.client.post('/summariser/', form_data, follow=True, format='multipart')
        self.assertEqual(response.status_code, 200,
                         "Correct status code: 200 actual response: %s" % response.status_code)
        self.assertTemplateUsed('input_error.html')

    @tag('fast', 'core')
    def test_form_invalid_remove_lists(self):
        """
        Testing the correct response to an invalid remove_list argument.
        """

        form_data = \
            {"url": english_test_url_bbc, "compression_rate": float(0.7), "remove_lists": 'foo', "file": None}
        response = self.client.post('/summariser/', form_data, follow=True, format='multipart')
        self.assertEqual(response.status_code, 200,
                         "Correct status code: 200 actual response: %s" % response.status_code)
        self.assertTemplateUsed('input_error.html')

    @tag('fast', 'core')
    def test_form_test_remove_false(self):
        """
        Testing the correct response to an invalid remove_list argument.
        """

        form_data = \
            {"url": english_test_url_bbc, "compression_rate": float(0.7), "remove_lists": False, "file": None}
        response = self.client.post('/summariser/', form_data, follow=True, format='multipart')
        self.assertEqual(response.status_code, 200,
                         "Correct status code: 200 actual response: %s" % response.status_code)
        self.assertTemplateUsed('summary_output.html')

    @tag('fast', 'core')
    def test_form_test_invalid_no_file_url(self):
        """
        Testing the correct response to an invalid arguments of no URL and no file.
        """

        form_data = \
                {"url": "", "compression_rate": float(0.7), "remove_lists": False, "file": None}
        response = self.client.post('/summariser/', form_data, follow=True, format='multipart')
        self.assertEqual(response.status_code, 200,
                         "Correct status code: 200 actual response: %s" % response.status_code)
        self.assertTemplateUsed('input_error.html')

    @tag('fast', 'core')
    def test_form_test_invalid_large_text(self):
        """
        Testing the correct response to an invalid argument of a too large text.txt file.
        """
        with open(large_english_test_text, "rb") as text:
            form_data = \
                {"url": "", "compression_rate": float(0.7), "remove_lists": False, "file": text}
            response = self.client.post('/summariser/', form_data, follow=True, format='multipart')
        self.assertEqual(response.status_code, 200,
                         "Correct status code: 200 actual response: %s" % response.status_code)
        self.assertTemplateUsed('input_error.html')

    @tag('fast', 'core')
    def test_form_test_invalid_file_type(self):
        """
        Method for testing the correct response to an invalid file type; text.foo
        """
        with open(invalid_file_type_text, "rb") as text:
            form_data = \
                {"url": "", "compression_rate": float(0.7), "remove_lists": False, "file": text}
            response = self.client.post('/summariser/', form_data, follow=True, format='multipart')
        self.assertEqual(response.status_code, 200,
                         "Correct status code: 200 actual response: %s" % response.status_code)
        self.assertTemplateUsed('input_error.html')