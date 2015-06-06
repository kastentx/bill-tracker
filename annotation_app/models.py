from django.db import models

class Bill(models.Model):
  text = models.TextField()

class Annotation(models.Model):
  reporter = models.ForeignKey(Bill)
  text = models.TextField()

class Comment(models.Model):
  reporter = models.ForeignKey(Annotation)
  text = models.TextField()
  