from django import forms
from .models import SubmitURL


class PostForm(forms.ModelForm):

    class Meta:
        model = SubmitURL
        fields = ("url", "compression_rate", "remove_lists", "file")