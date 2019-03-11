import os
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator


def validate_file_extension(value):
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.doc', '.docx', '.txt']
    if not ext.lower() in valid_extensions:
        raise ValidationError(u'Unsupported file extension.')


class FileValidator(RegexValidator):
    """
    Class for uploaded file validation.
    """
    def __init__(self, message=None):
        extensions = '.txt'
        if not hasattr(extensions, '__iter__'):
            extensions = [extensions]
        regex = '\.(%s)$' % '|'.join(extensions)
        if message is None:
            message = 'File type not supported. Accepted types are: %s.' % ', '.join(extensions)
        super(FileValidator, self).__init__(regex, message)

    def __call__(self, value):
        super(FileValidator, self).__call__(value.name)