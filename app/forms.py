from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator, URLValidator
from django.template.defaultfilters import filesizeformat
from app.validators import file_validator, url_validator, compression_rate_validator

CHOICES = ((True, 'Yes'),
               (False, 'No'),)

content_types = ['txt', ]


class PostForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)

    url = forms.URLField(required=False, validators=[url_validator], label='Write your URL here')
    file = forms.FileField(required=False, validators=[file_validator])
    compression_rate = forms.FloatField(min_value=0.0, max_value=1.0, validators=[compression_rate_validator])
    remove_lists = forms.ChoiceField(choices=CHOICES)

    def clean(self):
        data = self.cleaned_data
        if all(fields in data for fields in ('url','file', 'compression_rate', 'remove_lists')):
            if not bool(data['url']) and not bool(data['file']):  # if NOR file, url then throw error
                raise forms.ValidationError(message="You must enter either a URL or a text file to summarise",
                                  code='no_url_or_file')
            return data
        else:
            raise forms.ValidationError(message="GRS")


