# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.checks import messages

from app.article import Article
from skipthoughts import WebScraperSummation
from skipthoughts.textfileSummation import TextFileSummation

from django.shortcuts import render
from django.views.generic import TemplateView
from app.forms import PostForm
# Create your views here.
# app/views.py

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
        if request.method == 'GET':
            return render(request, 'summariser.html',  {'form': form})

    def post(self, request):
        if request.method == "POST":
            form = PostForm(request.POST)
            if form.is_valid():
                if bool(request.FILES.get('file', False)):  # check if a file has been uploaded
                    text_summariser = TextFileSummation()
                    sanitised_text = text_summariser.upload_txt(request)

                    summary_text = text_summariser.summarise_text_file(sanitised_text, form.data.get('compression_rate'))
                    article = Article(summary_text, form.data.get('url'), form.data.get('compression_rate'))  # Put into article object for easier indexing
                    return render(request, 'summary_output.html', {'article': article})  # Add article here

                else:  # Handle URL article
                    scraper = WebScraperSummation.WebScraperSummation()
                    summary_text = scraper.scrape(form.data.get('url'), False, float(form.data.get('compression_rate')))
                    article = Article(summary_text, form.data.get('url'), form.data.get('compression_rate'))  # Put into article object for easier indexing
                    return render(request, 'summary_output.html', {'article': article})  # Add article here

        return render(request, 'input_error.html', context=None)

