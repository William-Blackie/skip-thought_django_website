"""
Author: William Blackie
A file for holding test values to maintain consistency across test classes.
"""

# Testing variables.
import os

dirname = os.path.dirname(__file__)
path_to_test_data = os.path.join(dirname, r'test_files/')

# Test text files.
english_test_text = path_to_test_data + r'english_test.txt'
spanish_test_text = path_to_test_data + r'spanish_test.txt'
german_test_text = path_to_test_data + r'german_test.txt'

# Invalid text files.
large_english_test_text = path_to_test_data + r'large_english_test.txt'
invalid_file_type_text = path_to_test_data + r'english_test.foo'

# Differently Encoded text files.
ANSI_encoded_test_text = path_to_test_data + r'english_test_ANSI.txt'
unicode_encoded_test_text = path_to_test_data + r'english_test_unicode.txt'
unicode_big_encoded_test_text = path_to_test_data + r'english_test_unicode_b.txt'

# Test article urls.
english_test_url_bbc = r"https://www.bbc.co.uk/news/business-47287386"
english_test_url_new_york_times = r"https://www.nytimes.com/2019/03/14/learning/what-students-are-saying-about-female-superheroes-being-left-out-and-their-dream-homes.html"
english_test_url_thegaurdian = r"https://www.theguardian.com/environment/2019/mar/15/its-our-time-to-rise-up-youth-climate-strikes-held-in-100-countries"
spanish_test_url = r"https://cnnespanol.cnn.com/2019/03/11/fue-un-fin-de-semana-tragico-para-la-aviacion-hubo-3-accidentes-fatales/"
german_test_url = r"https://www.dw.com/de/flugzeugabsturz-in-aethiopien-un-mitarbeiter-und-deutsche-unter-den-toten/a-47846996"
