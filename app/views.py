# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from app.Article import Article
from skipthoughts import WebScraperSummation
from skipthoughts.TextfileSummation import TextFileSummation
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
            return render(request, 'summariser.html', {'form': form})

    def post(self, request):
        errors = {}
        if request.method == "POST":
            form = PostForm(request.POST, request.FILES)
            if form.is_valid():
                if bool(request.FILES.get('file', False)):  # check if a file has been uploaded
                    text_summariser = TextFileSummation()  # Handle text file article
                    summary_text, total_words, total_words_removed, errors = text_summariser.summarise_text_file(request, float(
                        form.data.get('compression_rate')), errors)
                    article = Article(summary_text, form.data.get('url'), form.data.get('compression_rate'),
                                      total_words, total_words_removed)  # Put into article object for easier indexing
                    if not errors:
                        return render(request, 'summary_output.html', {'article': article})  # Add article here

                else:  # Handle URL article
                    scraper = WebScraperSummation.WebScraperSummation()
                    summary_text, total_words, total_words_removed, errors = scraper.scrape(
                        form.data.get('url'), form.data.get("remove_lists"),
                        float(form.data.get('compression_rate')), errors)
                    if not errors:
                        article = Article(summary_text, form.data.get('url'), form.data.get('compression_rate'),
                                      total_words, total_words_removed)  # Put into article object for easier indexing
                        return render(request, 'summary_output.html', {'article': article})  # Add article here
            else:
                errors["invalid_post"] = form.errors
        return render(request, 'input_error.html', {'errors': errors})
