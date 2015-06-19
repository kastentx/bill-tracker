"""bill_tracker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
  https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
  1. Add an import:  from my_app import views
  2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
  1. Add an import:  from other_app.views import Home
  2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
  1. Add an import:  from blog import urls as blog_urls
  2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from annotation_app.controllers import annotations_controller,\
  comments_controller, clients_controller
# Deprecated
from annotation_app import views

urlpatterns = [
  # Bills routes
  url(r'^$', views.bill_list, name='bill_list'),
  url(r'^bills/$', views.bill_list, name='bills'),
  url(r'get_bill_list/$', views.get_bill_list, name='get_bill_list'),
  url(r'^addbill/$', views.add_bill, name='add_bill'),
  url(r'^bills/(?P<bill_id>\d+)/$', views.bill, name='bill'),

  # Authors routes
  url(r'^authors/$', views.author_list, name='authors'),
  url(r'get_author_list/$', views.get_author_list, name='get_author_list'),
  url(r'get_author_bills/$', views.get_author_bills, name='get_author_bills'),
  url(r'^authors/(?P<author_id>\d+)/$', views.author, name='author'),

  # Subjects routes
  url(r'^subjects/$', views.subject_list, name='subjects'),
  url(r'get_subject_list/$', views.get_subject_list, name='get_subject_list'),
  url(r'get_subject_bills/$', views.get_subject_bills,
    name='get_subject_bills'),
  url(r'^subjects/(?P<subject_id>\d+)/$', views.subject, name='subject'),

  # Annotations routes
  url(r'^annotations/$', annotations_controller.annotations,
    name='annotations'),
  url(r'^annotations/(?P<annotation_id>\d+)/$',
    annotations_controller.annotation, name='annotation'),

  # Comments routes
  url(r'^addcomment/$', comments_controller.add_comment, name='add_comment'),
  url(r'^comments/(?P<comment_id>\d+)/$', comments_controller.comment,
    name='comment'),
  url(r'^comments/(?P<comment_id>\d+)/edit/$', comments_controller.edit_comment,
    name='edit_comment'),

  # Frontend examples routes
  url(r'^example-client/$', clients_controller.example_client,
    name='example_client'),
  url(r'^megalith/$', clients_controller.megalith, name='megalith'),

  # Deprecated
  # url(r'^index/$', views.index),
  # url(r'^addannotation/$', views.add_annotation, name='add_annotation'),
]
