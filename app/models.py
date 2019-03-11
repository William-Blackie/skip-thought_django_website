# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re

from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator, FileExtensionValidator
from django.db import models


# Create your models here.


regex = re.compile(
            r'^(?:http|ftp)s?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)

CHOICES = ((True, 'Yes'),
               (False, 'No'),)

class SubmitForm(models.Model):
    url = models.URLField('URL:', blank=True)
    file = models.FileField(upload_to="app/data/temp_docs", validators=[FileExtensionValidator(['.txt'])], blank=True)
    compression_rate = models.FloatField(validators=[MinValueValidator(0.1), MaxValueValidator(1.0)], default=0.7)

    CHOICES = ((True, 'Yes'),
               (False, 'No'),)

    remove_lists = models.NullBooleanField(max_length=2, choices=CHOICES, default=True)

    def publish(self):
        self.save()

    def clean(self):
        if not bool(self.url) and bool(self.file):  # if NOR file, url then throw error
            raise ValidationError(message="You must enter either a URL or a text file to summarise", code='no_url_or_file')
        elif self.compression_rate > 1.0 or self.compression_rate < 0.1:
            raise ValidationError(message="Compression rate out of bounds: (0.1-1.0): actual %s " % self.compression_rate, code='compression_rate_out_of_bounds')
        elif re.match(regex, str(self.url)) is False:
            raise ValidationError(message="URL not valid: url found: %s " % self.url, code='invalid_url')
        elif self.remove_lists not in (True, False):
            raise ValidationError(message="remove_lists not in choices, choice found: %s " % str(self.remove_lists), code='invalid_remove_lists')

