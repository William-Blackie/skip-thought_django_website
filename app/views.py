# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
# app/views.py
from django.shortcuts import render
from django.views.generic import TemplateView


# Create your views here.
from app.forms import PostForm


class HomePageView(TemplateView):
    def get(self, request, **kwargs):
        return render(request, 'index.html', context=None)


class AboutPageView(TemplateView):
    def get(self, request, **kwargs):
        return render(request, 'about.html', context=None)


class ResearchPageView(TemplateView):
    def get(self, request, **kwargs):
        return render(request, 'research.html', context=None)


class SummariserPageView(TemplateView):
    def get(self, request, **kwargs):
        form = PostForm()
        return render(request, 'summariser.html',  {'form': form})

    def post(self, request, *args, **kwargs):
        if request.method == "POST":
            form = PostForm(request.POST)
            if form.is_valid():
                print form.data.get('url')
                print form.data.get('compression_rate')
                print form.data.get('remove_lists')
                return render(request, )

        return render(request, 'input_error.html', context=None)
