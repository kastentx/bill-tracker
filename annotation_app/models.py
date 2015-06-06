from django.db import models

class Bill(models.Model):
  text = models.TextField()

class Annotation(models.Model):
  bill_id = models.ForeignKey(Bill)
  sentence_id = models.PositiveIntegerField()
  text = models.TextField()

class Comment(models.Model):
  annotation_id = models.ForeignKey(Annotation)
  text = models.TextField()
  