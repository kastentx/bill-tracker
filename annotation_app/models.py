from django.db import models
from flask import json


class Bill(models.Model):
  text = models.TextField()
  number = models.IntegerField(default=0)
  stage = models.IntegerField(default=0)
  origin = models.CharField(max_length=255, default="null")
  last_action = models.CharField(max_length=255, default= "null")
  caption_version = models.CharField(max_length=255, default= "null")
  caption_text = models.TextField(default="null")
  coauthor = models.CharField(max_length=255, default= "null")
  sponsor = models.CharField(max_length=255, default="null")
  cosponsor = models.CharField(max_length=255, default= "null")
  subjects = models.TextField(default="null")

  def serialize(object):
    return json.dumps(object)

  def deserialize(object):
    return json.loads(object)

class Senator(models.Model):
  name = models.CharField(max_length=255)
  committee = models.CharField(max_length=255)
  is_chair = models.BooleanField()
  bills = models.ManyToManyField(Bill)



class Annotation(models.Model):
  bill_id = models.ForeignKey(Bill)
  sentence_id = models.PositiveIntegerField(null=True)
  text = models.TextField()

class Comment(models.Model):
  annotation_id = models.ForeignKey(Annotation)
  text = models.TextField()
  