# _*_ coding:utf-8 _*_
"""
Created on 2015-05-24

@author: lujin
"""
from django.conf.urls import url, include

urlpatterns = [
    url(r'article/', include('app.article.urls', namespace='article')),
    url(r'login/', include('app.login.urls', namespace='login')),
    url(r'setup/', include('app.setup.urls', namespace='setup')),
]