from django.db import models
import json


class Bill(models.Model):
  text = models.TextField()
  number = models.IntegerField(default=0)
  stage = models.IntegerField(default=0)
  origin = models.CharField(max_length=255, default="null")
  last_action = models.CharField(max_length=255, default= "null")
  caption_version = models.CharField(max_length=255, default= "null")
  caption_text = models.TextField(default="null")
  coauthors = models.CharField(max_length=255, default= "null")
  sponsors = models.CharField(max_length=255, default="null")
  cosponsors = models.CharField(max_length=255, default= "null")
  subjects = models.TextField(default="null")
  authors = models.TextField(default="null")

  def serialize(object):
    return json.dumps(object)

  def deserialize(object):
    return json.loads(object)

class Senator(models.Model):
  name = models.CharField(max_length=255)
  committee = models.CharField(max_length=255)
  is_chair = models.BooleanField()
  bills = models.ManyToManyField(Bill)

class Subject(models.Model):
  name = models.CharField(max_length=255)
  bills = models.ManyToManyField(Bill)


class Annotation(models.Model):
  user = models.CharField(max_length=255, default="demoUser")
  bill = models.ForeignKey(Bill)
  # sentence_id = models.PositiveIntegerField(null=True)

  created = models.DateTimeField(auto_now_add=True, null=True)
  # updated = models.DateTimeField(auto_now=True)
  text = models.TextField(null=True)
  quote = models.TextField(null=True)
  # uri = models.CharField(max_length=255)

  # ranges_start = models.CharField(max_length=255)
  # ranges_end = models.CharField(max_length=255)
  ranges_start_offset = models.IntegerField(null=True)
  ranges_end_offset = models.IntegerField(null=True)

  tags = models.TextField(default="[]")

  permissions_read = models.CharField(max_length=255, null=True)

# JSON:
# {
#   'id': 1434156917830,              # unique id (added by backend)
#   'bill_id': 1,                     # bill id it belongs to (added by backend)
#   'text': 'Clinton',                # content of annotation
#   'quote': 'BILL',                  # the annotated text (added by frontend)
#   'ranges': [{                      # list of ranges covered by annotation (usually only one entry)
#     'start': '',                    # (relative) XPath to start element
#     'end': '',                      # (relative) XPath to end element
#     'startOffset': 79,              # character offset within start element
#     'endOffset': 83                 # character offset within end element
#   }],
#   'tags': ['Former', 'president'],  # list of tags (from Tags plugin)
#   'user': 'demoUser',               # user id of annotation owner (can also be an object with an 'id' property)
#   'permissions': {                  # annotation permissions (from Permissions/AnnotateItPermissions plugin)
#     'read': [],
#     'update': ['demoUser'],
#     'delete': ['demoUser'],
#     'admin': ['demoUser']
#   },
#   'data_creacio': 1434156917763     # created datetime in iso8601 format (added by backend)
# }

class Comment(models.Model):
  annotation = models.ForeignKey(Annotation)
  text = models.TextField()
