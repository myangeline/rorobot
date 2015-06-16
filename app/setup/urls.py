# _*_ coding:utf-8 _*_
"""
Created on 2015-06-13

@author: lujin
"""
from django.conf.urls import url
from app.setup import views

urlpatterns = [
    url(r'^website/$', views.website),
    url(r'^personal/$', views.personal),
]