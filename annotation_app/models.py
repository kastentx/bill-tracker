from django.db import models

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


class Senator(models.Model):
  name = models.CharField(max_length=255)
  committee = models.CharField(max_length=255)
  is_chair = models.BooleanField()
  bills = models.ManyToManyField(Bill)



class Annotation(models.Model):
  reporter = models.ForeignKey(Bill)
  text = models.TextField()

class Comment(models.Model):
  reporter = models.ForeignKey(Annotation)
  text = models.TextField()
  