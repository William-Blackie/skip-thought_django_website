# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from app.article import Article
from skipthoughts import WebScraperSummation
import thread

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
    def get(self, request):
        form = PostForm()
        return render(request, 'summariser.html',  {'form': form})

    def post(self, request):
        if request.method == "POST":
            form = PostForm(request.POST)
            if form.is_valid():
                print form.data.get('url')
                print form.data.get('compression_rate')
                print form.data.get('remove_lists')
                scraper = WebScraperSummation.WebScraperSummation()
                summary_text = scraper.scrape(form.data.get('url'), False, float(form.data.get('compression_rate')))
                del scraper
                article = Article(summary_text, form.data.get('url'), form.data.get('compression_rate'))  # Put into article object for easier indexing
                return render(request, 'summary_output.html', {'article': article})  # Add article here

        return render(request, 'input_error.html', context=None)
