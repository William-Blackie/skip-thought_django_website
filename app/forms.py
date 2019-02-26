from django import forms
from .models import submitURL


class PostForm(forms.ModelForm):

    class Meta:
        model = submitURL
        fields = ("url", "compression_rate", "remove_lists")