import StringIO
import os

from django.core.files.base import ContentFile
from django.test import TestCase, RequestFactory
from app.forms import PostForm
from django.core.files.uploadedfile import SimpleUploadedFile, InMemoryUploadedFile
from django.core.files.uploadedfile import File
from app.views import SummariserPageView
from django.test import Client

# Testing variables
dirname = os.path.dirname(__file__)
path_to_test_data = os.path.join(dirname, r'test_files/')
english_test_text = path_to_test_data + r'english_test.txt'
spanish_test_text = path_to_test_data + r'spanish_test.txt'
german_test_text = path_to_test_data + r'german_test.txt'


class TestSummariser(TestCase):
    """

    """
    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()

    def test_summarise_text_file_english(self):
        """
        Method for testing the correct response for an english .txt file.
        """
        with open(english_test_text, "rb") as text:
            form_data = \
                {"url": "", "compression_rate": 0.7, "remove_lists": True, "file": text}
            response = self.client.post('/summariser/', form_data, follow=True, format='multipart')
        self.assertEqual(response.status_code, 200,
                         "Correct status code: 200 actual response: %s" % response.status_code)
        self.assertTemplateUsed('summary_output.html')

    def test_summarise_text_file_spanish(self):

        with open(spanish_test_text, "rb") as text:
            form_data = \
                {"url": "", "compression_rate": 0.7, "remove_lists": True,
                 "file": text}
            response = self.client.post('/summariser/', form_data, follow=True, format='multipart')
        self.assertEqual(response.status_code, 200,
                         "Correct status code: 200 actual response: %s" % response.status_code)
        self.assertTemplateUsed('input_error.html')

    def test_summarise_text_file_german(self):
        with open(german_test_text, "rb") as text:
            form_data = \
                {"url": "", "compression_rate": 0.7, "remove_lists": True,
                 "file": text}
            response = self.client.post('/summariser/', form_data, follow=True, format='multipart')
        self.assertEqual(response.status_code, 200, "Correct status code: 200 actual response: %s" % response.status_code)
        self.assertTemplateUsed('input_error.html')


class TestForms(TestCase):
    def test_form_url(self):
        form_data = {"url": "https://www.bbc.co.uk/news/business-47287386",
                     "compression_rate": 0.7,
                     "remove_lists": True,
                     "file": None}
        form = PostForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_invalid_url(self):
        form_data = {"url": "test_value",
                     "compression_rate": 0.7,
                     "remove_lists": True,
                     "file": None}
        form = PostForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_form_invalid_compression_rate_upper(self):
        form_data = {"url": "test_value",
                     "compression_rate": 1.1,
                     "remove_lists": True,
                     "file": None}
        form = PostForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_form_invalid_compression_rate_lower(self):
        form_data = {"url": "test_value",
                     "compression_rate": -1,
                     "remove_lists": True,
                     "file": None}
        form = PostForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_form_upload_txt(self):
        test_file = SimpleUploadedFile("file.txt",
                                       "file_content",
                                       content_type="text/pdf")
        form_data = {"url": None,
                     "compression_rate": 0.7,
                     "remove_lists": True,
                     "file": test_file}
        form = PostForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_invalid_file(self):
        test_file = SimpleUploadedFile("file.foo",
                                       "file_content",
                                       content_type="text/pdf")
        form_data = {"url": None,
                     "compression_rate": 0.7,
                     "remove_lists": True,
                     "file": test_file}
        form = PostForm(data=form_data)
        self.assertFalse(form.is_valid())

    # TODO add validation for file size

class TestViews(TestCase):
    def setUp(self):
        self.client = Client()

    def test_about_view(self):
        """

        :return:
        """
        response = self.client.get('/about/', follow=True)
        self.assertEqual(response.status_code, 200,
                         "Correct status code: 200 actual response: %s" % response.status_code)
        self.assertTemplateUsed('about.html')

    def test_research_view(self):
        """

        :return:
        """
        response = self.client.get('/research/', follow=True)
        self.assertEqual(response.status_code, 200,
                         "Correct status code: 200 actual response: %s" % response.status_code)
        self.assertTemplateUsed('about.html')

    def test_home_view(self):
        """

        :return:
        """
        response = self.client.get('/', follow=True)
        self.assertEqual(response.status_code, 200,
                         "Correct status code: 200 actual response: %s" % response.status_code)
        self.assertTemplateUsed('index.html')

    def test_summariser_view(self):
        """

        :return:
        """
        response = self.client.get('/summariser/', follow=True)
        self.assertEqual(response.status_code, 200,
                         "Correct status code: 200 actual response: %s" % response.status_code)
        self.assertTemplateUsed('summariser.html')