from django import forms
from app.validators import file_validator, url_validator, compression_rate_validator

"""
Author: William Blackie
Class for creating my PostForm.
"""

# Static variables.
CHOICES = ((True, 'Yes'),
           (False, 'No'),)

CONTENT_TYPES = ['txt', ]


class PostForm(forms.Form):
    def __init__(self, *args, **kwargs):
        """
        Basic init method.
        :param args: url, file, compression_rate and remove_lists.
        :param kwargs:
        """
        super(PostForm, self).__init__(*args, **kwargs)

    url = forms.URLField(required=False, validators=[url_validator], label='Write your URL here')
    file = forms.FileField(required=False, validators=[file_validator], label='Or upload a text.txt file')
    compression_rate = forms.FloatField(min_value=0.1, max_value=1.0, validators=[compression_rate_validator],
                                        initial=0.7)
    remove_lists = forms.ChoiceField(choices=CHOICES)

    def clean(self):
        """
        Method overriding default clean method, allowing custom validators to be called in self.cleaned.
        Allowing for checking for custom inputs at upload time.
        :return: data: sanitised form object.
        """
        data = self.cleaned_data
        if all(fields in data for fields in ('url', 'file', 'compression_rate', 'remove_lists')):
            if not bool(data['url']) and not bool(data['file']):  # if NOR file, url then throw error
                raise forms.ValidationError(message="You must enter either a URL or a text file to summarise",
                                            code='no_url_or_file')
            return data
        else:
            raise forms.ValidationError(message="GRS")
