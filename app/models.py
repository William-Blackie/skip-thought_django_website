# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django import forms

# Create your models here.


class submitURL(models.Model):
    url = models.URLField('URL:')
    compression_rate = models.FloatField(validators=[MinValueValidator(0.1), MaxValueValidator(1.0)], default=0.7)

    CHOICES =((True, 'Yes'),
               (False, 'No'),)

    remove_lists = models.NullBooleanField(max_length=2, choices=CHOICES, default=True)

    def publish(self):
        self.save()