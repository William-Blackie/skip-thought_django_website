import os
import django
from django.test import TestCase, tag
from app.forms import PostForm
from app.test import english_test_url_bbc

"""
Author: William Blackie
Class for testing app.PostForm creation.
"""

# Set environment variables to allow running of class individually.
os.environ['DJANGO_SETTINGS_MODULE'] = 'skipthought_django_website.settings'
django.setup()


class TestForms(TestCase):
    @staticmethod
    def create_form(url, compression_rate, remove_lists, uploaded_file):
        """
        Simple method to create a PostForm.
        :param url: String URL
        :param compression_rate: Float (0.1-1.0)
        :param remove_lists: Bool (True, False)
        :param uploaded_file: File
        :return: PostForm object
        """
        return PostForm({'url': url,
                         'compression_rate': compression_rate,
                         'remove_lists': remove_lists,
                         'file': uploaded_file})

    @tag('fast')
    def test_form(self):
        """
        Simple method to create and test a PostForm being valid.
        """
        form = self.create_form(url=english_test_url_bbc,
                                compression_rate=0.7,
                                remove_lists=True,
                                uploaded_file=None)
        self.assertTrue(form.is_valid())