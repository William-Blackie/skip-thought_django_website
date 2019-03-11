import os
from contextlib import contextmanager

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase, RequestFactory
from app.forms import PostForm
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client
from django.core.files import File
from app.models import SubmitForm

# Testing variables
dirname = os.path.dirname(__file__)
path_to_test_data = os.path.join(dirname, r'test_files/')

# Test text files
english_test_text = path_to_test_data + r'english_test.txt'
spanish_test_text = path_to_test_data + r'spanish_test.txt'
german_test_text = path_to_test_data + r'german_test.txt'

# Test article urls
english_test_url = r"https://www.bbc.co.uk/news/business-47287386"
spanish_test_url = r"https://cnnespanol.cnn.com/2019/03/11/fue-un-fin-de-semana-tragico-para-la-aviacion-hubo-3-accidentes-fatales/"
german_test_url = r"https://www.dw.com/de/flugzeugabsturz-in-aethiopien-un-mitarbeiter-und-deutsche-unter-den-toten/a-47846996"


class TestSummariser(TestCase):
    """

    """
    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()

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
    def test_form_url(self):
        form_data = {"url": english_test_url,
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
        form_data = {"url": english_test_url,
                     "compression_rate": 1.1,
                     "remove_lists": True,
                     "file": None}
        form = PostForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_form_invalid_compression_rate_lower(self):
        form_data = {"url": english_test_url,
                     "compression_rate": -1,
                     "remove_lists": True,
                     "file": None}
        form = PostForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_form_upload_txt(self):
        with open(english_test_text, "rb") as text:
            form_data = {"url": None,
                     "compression_rate": 0.7,
                     "remove_lists": True,
                     "file": File(text)}
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


class TestModels(TestCase):
    def setUp(self):
        self.user = User()
        self.client = Client()
    @staticmethod
    def create_model_SubmitForm(url, compression_rate, remove_lists, my_file):
        return SubmitForm.objects.create(
                          url=url,
                          compression_rate=compression_rate,
                          remove_lists=remove_lists,
                          file=my_file)

    def test_Model_no_url_file(self):
        model = self.create_model_SubmitForm(
            url=None,
            compression_rate=0.7,
            remove_lists=True,
            my_file=None)
        raised = False
        try:
            model.full_clean()
        except ValidationError as e:
            print e.messages
            raised = True
        self.assertTrue(raised, 'Exception raised')

    def test_Model_no_file(self):
        model = self.create_model_SubmitForm(
                url=english_test_url,
                compression_rate=0.7,
                remove_lists=True,
                my_file=None)
        raised = False
        try:
            model.full_clean()
        except ValidationError as e:
            print e.messages
            raised = True
        self.assertFalse(raised, 'Exception raised')

    def test_model_upper_compression(self):
        model = self.create_model_SubmitForm(
            url=english_test_url,
            compression_rate=1.1,
            remove_lists=True,
            my_file=None)
        try:
            model.full_clean()
            self.fail('Validation Error should be raised')
        except ValidationError as e:
            raised = True
        self.assertTrue(raised, 'Exception raised')

    def test_model_lower_compression(self):
        model = self.create_model_SubmitForm(
            url=english_test_url,
            compression_rate=-1,
            remove_lists=True,
            my_file=None)
        try:
            model.full_clean()
            self.fail('Validation Error should be raised')
        except ValidationError as e:
            raised = True
        self.assertTrue(raised, 'Exception raised')

    def test_model_remove_lists_false(self):
        model = self.create_model_SubmitForm(
            url=english_test_url,
            compression_rate=0.7,
            remove_lists=False,
            my_file=None)

        raised = False
        try:
            model.full_clean()
        except ValidationError as e:
            print e.messages
            raised = True
        self.assertFalse(raised, 'Exception raised')



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