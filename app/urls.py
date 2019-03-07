# app/urls.py
from django.conf.urls import url
from django.views.generic import RedirectView

from app import views

urlpatterns = [
    url(r'^$', views.HomePageView.as_view()),
    url(r'^about/$', views.AboutPageView.as_view()),
    url(r'^summariser/$', views.SummariserPageView.as_view()),
    url(r'^research/$', views.ResearchPageView.as_view()),
    url(r'^favicon.ico$', RedirectView.as_view(url='/static/images/favicon.ico')),

]

