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
#   "id": "39fc339cf058bd22176771b3e3187329",  # unique id (added by backend)
#   "annotator_schema_version": "v1.0",        # schema version: default v1.0
#   "created": "2011-05-24T18:52:08.036814",   # created datetime in iso8601 format (added by backend)
#   "updated": "2011-05-26T12:17:05.012544",   # updated datetime in iso8601 format (added by backend)
#   "text": "A note I wrote",                  # content of annotation
#   "quote": "the text that was annotated",    # the annotated text (added by frontend)
#   "uri": "http://example.com",               # URI of annotated document (added by frontend)
#   "ranges": [                                # list of ranges covered by annotation (usually only one entry)
#     {
#       "start": "/p[69]/span/span",           # (relative) XPath to start element
#       "end": "/p[70]/span/span",             # (relative) XPath to end element
#       "startOffset": 0,                      # character offset within start element
#       "endOffset": 120                       # character offset within end element
#     }
#   ],
#   "user": "alice",                           # user id of annotation owner (can also be an object with an 'id' property)
#   "consumer": "annotateit",                  # consumer key of backend
#   "tags": [ "review", "error" ],             # list of tags (from Tags plugin)
#   "permissions": {                           # annotation permissions (from Permissions/AnnotateItPermissions plugin)
#     "read": ["group:__world__"],
#     "admin": [],
#     "update": [],
#     "delete": []
#   }
# }

class Comment(models.Model):
  annotation = models.ForeignKey(Annotation)
  text = models.TextField()
