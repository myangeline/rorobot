# _*_ coding:utf-8 _*_
"""
Created on 2015-05-24

@author: lujin
"""
from django.conf.urls import url
from app.login import views

urlpatterns = [
    url(r'^$', views.login),
]
