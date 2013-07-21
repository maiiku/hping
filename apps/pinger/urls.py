# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from apps.pinger.views import HaystackUploadView, HaystackCreateView, HaystackListView, HaystackUpdateView, HaystackDeleteView

urlpatterns = patterns('',
    url(r'upload/$', HaystackUploadView.as_view(), name='hay_upload'),
    url(r'add/$', HaystackCreateView.as_view(), name='hay_add'),
    url(r'list/$', HaystackListView.as_view(), name='hay_list'),
    url(r'list/(?P<pk>\d+)/$', HaystackUpdateView.as_view(), name='hay_update'),
    url(r'list/(?P<pk>\d+)/delete/$', HaystackDeleteView.as_view(), name='hay_delete'),

    url(r'$', HaystackListView.as_view(), name='home'),
)
