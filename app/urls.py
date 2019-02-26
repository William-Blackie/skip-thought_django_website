# app/urls.py
from django.conf.urls import url
from app import views


urlpatterns = [
    url(r'^$', views.HomePageView.as_view()),
    url(r'^about/$', views.AboutPageView.as_view()),
    url(r'^summariser/$', views.SummariserPageView.as_view()),

]