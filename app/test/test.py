import os
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase, RequestFactory, tag
from app.forms import PostForm
from django.core.files.uploadedfile import SimpleUploadedFile, InMemoryUploadedFile
from django.test import Client

# Testing variables
dirname = os.path.dirname(__file__)
path_to_test_data = os.path.join(dirname, r'test_files/')

# Test text files
english_test_text = path_to_test_data + r'english_test.txt'
spanish_test_text = path_to_test_data + r'spanish_test.txt'
german_test_text = path_to_test_data + r'german_test.txt'
large_english_test_text = path_to_test_data + r'large_english_test.txt'
bad_file_type_text = path_to_test_data + r'english_test.foo'

# Test article urls
english_test_url = r"https://www.bbc.co.uk/news/business-47287386"
spanish_test_url = r"https://cnnespanol.cnn.com/2019/03/11/fue-un-fin-de-semana-tragico-para-la-aviacion-hubo-3-accidentes-fatales/"
german_test_url = r"https://www.dw.com/de/flugzeugabsturz-in-aethiopien-un-mitarbeiter-und-deutsche-unter-den-toten/a-47846996"


class TestFormValidation(TestCase):
    def setUp(self):
        self.client = Client()

    @tag('fast', 'core')
    def test_form_bad_url(self):
        """
        Method for testing the correct response for an english.txt file.
        """

        form_data = \
                {"url": "foobar", "compression_rate": float(0.7), "remove_lists": True, "file": None}
        response = self.client.post('/summariser/', form_data, follow=True, format='multipart')
        self.assertEqual(response.status_code, 200,
                         "Correct status code: 200 actual response: %s" % response.status_code)
        self.assertTemplateUsed('input_error.html')

    @tag('fast', 'core')
    def test_form_bad_upper_compression(self):
        """
        Method for testing the correct response for an english.txt file.
        """

        form_data = \
            {"url": english_test_url, "compression_rate": float(1.1), "remove_lists": True, "file": None}
        response = self.client.post('/summariser/', form_data, follow=True, format='multipart')
        self.assertEqual(response.status_code, 200,
                         "Correct status code: 200 actual response: %s" % response.status_code)
        self.assertTemplateUsed('input_error.html')

    @tag('fast', 'core')
    def test_form_bad_remove_lists(self):
        """
        Method for testing the correct response for an english.txt file.
        """

        form_data = \
            {"url": english_test_url, "compression_rate": float(0.7), "remove_lists": 'foo', "file": None}
        response = self.client.post('/summariser/', form_data, follow=True, format='multipart')
        self.assertEqual(response.status_code, 200,
                         "Correct status code: 200 actual response: %s" % response.status_code)
        self.assertTemplateUsed('input_error.html')

    @tag('fast', 'core')
    def test_form_test_remove_false(self):
        """
        Method for testing the correct response for an english.txt file.
        """

        form_data = \
            {"url": english_test_url, "compression_rate": float(1.1), "remove_lists": False, "file": None}
        response = self.client.post('/summariser/', form_data, follow=True, format='multipart')
        self.assertEqual(response.status_code, 200,
                         "Correct status code: 200 actual response: %s" % response.status_code)
        self.assertTemplateUsed('summary_output.html')


    @tag('fast', 'core')
    def test_form_bad_lower_compression(self):
        """
        Method for testing the correct response for an english.txt file.
        """

        form_data = \
            {"url": english_test_url, "compression_rate": float(-1.0), "remove_lists": True, "file": None}
        response = self.client.post('/summariser/', form_data, follow=True, format='multipart')
        self.assertEqual(response.status_code, 200,
                         "Correct status code: 200 actual response: %s" % response.status_code)
        self.assertTemplateUsed('input_error.html')

    @tag('fast', 'core')
    def test_form_test_no_file_url(self):
        """
        Method for testing the correct response for an english.txt file.
        """
        with open(large_english_test_text, "rb") as text:
            form_data = \
                {"url": "", "compression_rate": float(0.7), "remove_lists": False, "file": None}
            response = self.client.post('/summariser/', form_data, follow=True, format='multipart')
        self.assertEqual(response.status_code, 200,
                         "Correct status code: 200 actual response: %s" % response.status_code)
        self.assertTemplateUsed('input_error.html')

    @tag('fast', 'core')
    def test_form_test_large_text(self):
        """
        Method for testing the correct response for an english.txt file.
        """
        with open(large_english_test_text, "rb") as text:
            form_data = \
                {"url": "", "compression_rate": float(0.7), "remove_lists": False, "file": text}
            response = self.client.post('/summariser/', form_data, follow=True, format='multipart')
        self.assertEqual(response.status_code, 200,
                         "Correct status code: 200 actual response: %s" % response.status_code)
        self.assertTemplateUsed('input_error.html')

    @tag('fast', 'core')
    def test_form_test_bad_file_type(self):
        """
        Method for testing the correct response for an english.txt file.
        """
        with open(bad_file_type_text, "rb") as text:
            form_data = \
                {"url": "", "compression_rate": float(0.7), "remove_lists": False, "file": text}
            response = self.client.post('/summariser/', form_data, follow=True, format='multipart')
        self.assertEqual(response.status_code, 200,
                         "Correct status code: 200 actual response: %s" % response.status_code)
        self.assertTemplateUsed('input_error.html')

class TestSummariser(TestCase):
    """

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
                {"url": "", "compression_rate": float(0.7), "remove_lists": True, "file": text}
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
                {"url": "", "compression_rate": float(0.7), "remove_lists": True,
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
                {"url": "", "compression_rate": 0.7, "remove_lists": True,
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
            {"url": english_test_url,
             "compression_rate": float(0.7),
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
             "compression_rate": 0.7,
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
             "compression_rate": 0.7,
             "remove_lists": True,
            "file": None}
        response = self.client.post('/summariser/', form_data, follow=True, format='multipart')
        self.assertEqual(response.status_code, 200, "Correct status code: 200 actual response: %s" % response.status_code)
        self.assertTemplateUsed('input_error.html')


class TestForms(TestCase):
    @staticmethod
    def create_form(url, compression_rate, remove_lists, file):
        return PostForm({'url': url, 'compression_rate': compression_rate, 'remove_lists': remove_lists, 'file': file})

    @tag('fast')
    def test_form_url(self):
        form = self.create_form(url=english_test_url, compression_rate=0.7, remove_lists=True, file=None)
        self.assertTrue(form.is_valid())



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