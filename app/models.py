# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator, FileExtensionValidator
from django.db import models
from .validators import validate_file_extension


# Create your models here.


class SubmitForm(models.Model):
    url = models.URLField('URL:', blank=True)
    file = models.FileField(upload_to="app/data/temp_docs", validators=[FileExtensionValidator(['txt'])], blank=True)
    compression_rate = models.FloatField(validators=[MinValueValidator(0.1), MaxValueValidator(1.0)], default=0.7)

    CHOICES = ((True, 'Yes'),
               (False, 'No'),)

    remove_lists = models.NullBooleanField(max_length=2, choices=CHOICES, default=True)

    def publish(self):
        self.save()

    def clean(self):
        if not (len(self.url) > 0 or self.file is not None):
            raise ValidationError("You must enter either a URL or a text file to summarise")
