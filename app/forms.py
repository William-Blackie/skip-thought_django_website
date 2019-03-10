from django import forms
from .models import SubmitForm


class PostForm(forms.ModelForm):
    class Meta:
        model = SubmitForm
        fields = ("url", "compression_rate", "remove_lists", "file")