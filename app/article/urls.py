# _*_ coding:utf-8 _*_
from app.article import views

__author__ = 'lujin'

from django.conf.urls import url

urlpatterns = [
    url(r'^$', views.index),
    url(r'^category/$', views.category),
    url(r'^add-category/$', views.add_category),
    url(r'^check-category-name/$', views.check_category_name),
]
