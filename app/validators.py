import os
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.template.defaultfilters import filesizeformat

"""
Author: William Blackie
Methods for custom field validation.
"""


def file_validator(uploaded_file):
    """
    Method for verifying valid file extension(only .txt) and file size(<10kb).
    :param uploaded_file: File Object.
    """
    ext = os.path.splitext(uploaded_file.name)[1]  # [0] returns path+filename
    valid_extensions = ['.txt']
    if not ext.lower() in valid_extensions:
        raise ValidationError(u'Unsupported file extension.')
    if uploaded_file.size > 10024:  # 10KB file maximum
        raise ValidationError(message='Please keep file size under %s. Current file size %s' % (
            filesizeformat(10024), filesizeformat(uploaded_file.size)))


def url_validator(url):
    """
    Method for validating a valid URL using django URLValidator.
    :param url: String URL.
    """
    validate = URLValidator()
    try:
        validate(url)
    except ValidationError:
        raise ValidationError(message="Invalid URL: %s0=" % url,
                              code='Invalid_url')


def compression_rate_validator(compression_rate):
    """
    Method for validation of compression_rate bounds: (0.1-1.0).
    :param compression_rate: Float (0.1-1.0).
    """
    if compression_rate > 1.0 or compression_rate < 0.1:
        raise ValidationError(message="Compression rate out of bounds: (0.1-1.0): actual %s " % compression_rate,
                code='compression_rate_out_of_bounds')


def remove_lists_validator(remove_lists):
    """
    Method for validation of remove_list bounds: (True, False).
    :param remove_lists: Bool (True, False)
    """
    if remove_lists not in (u'True', u'False'):
        raise ValidationError(message="remove_lists not in choices, choice found: %s " % str(remove_lists),
                                  code='invalid_remove_lists')