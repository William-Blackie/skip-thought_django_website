import os
import django
from django.test import TestCase, Client

"""
Author: William Blackie
Class for testing views being correctly shown.
"""

# Set environment variables to allow running of class individually.
os.environ['DJANGO_SETTINGS_MODULE'] = 'skipthought_django_website.settings'
django.setup()


class TestViews(TestCase):
    def setUp(self):
        self.client = Client()

    def test_about_view(self):
        """
        method for testing the correct view is shown from GET method.
        :return: None.
        """
        response = self.client.get('/about/', follow=True)
        self.assertEqual(response.status_code, 200,
                         "Correct status code: 200 actual response: %s" % response.status_code)
        self.assertTemplateUsed('about.html')

    def test_research_view(self):
        """
        method for testing the correct view is shown from GET method.
        :return: None.
        """
        response = self.client.get('/research/', follow=True)
        self.assertEqual(response.status_code, 200,
                         "Correct status code: 200 actual response: %s" % response.status_code)
        self.assertTemplateUsed('research.html')

    def test_home_view(self):
        """
        method for testing the correct view is shown from GET method.
        :return: None.
        """
        response = self.client.get('/', follow=True)
        self.assertEqual(response.status_code, 200,
                         "Correct status code: 200 actual response: %s" % response.status_code)
        self.assertTemplateUsed('index.html')

    def test_summariser_view(self):
        """
        method for testing the correct view is shown from GET method.
        :return: None.
        """
        response = self.client.get('/summariser/', follow=True)
        self.assertEqual(response.status_code, 200,
                         "Correct status code: 200 actual response: %s" % response.status_code)
        self.assertTemplateUsed('summariser.html')