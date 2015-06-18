from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from annotation_app.models import Comment, Annotation
from annotation_app.forms import CommentAddForm, CommentEditForm

def add_comment(request):
  if request.method == 'POST':
    if 'add_for' in request.POST:
      form = CommentAddForm(initial={'annotation': comment.annotation})
      return render(request, 'addcomment.html',
        {'form': form, 'method': 'add'})
    else:
      form = CommentAddForm(request.POST)
      if form.is_valid():
        data = form.cleaned_data
        r = Comment()
        r.annotation = Annotation.objects.get(id = request.POST['annotation'])
        r.text = data['text']
        r.save()
        return HttpResponseRedirect('/comments/%d/' % r.id)
  raise Http404

def comment(request, comment_id):
  try:
    comment = Comment.objects.get(id = comment_id)
  except Comment.DoesNotExist:
    raise Http404
  context = {'comment': comment}
  return render(request, 'comment.html', context)

def edit_comment(request, comment_id):
  try:
    comment = Comment.objects.get(id = comment_id)
  except Comment.DoesNotExist:
    raise Http404

  if request.method == 'POST':
    form = CommentEditForm(request.POST)
    if form.is_valid():
      data = form.cleaned_data
      comment.text = data['text']
      comment.save()
      return HttpResponseRedirect('/comments/%d/' % comment.id)
  else:
    form = CommentEditForm(initial={'id': comment.id,
      'annotation': comment.annotation, 'text': comment.text})
  return render(request, 'commentform.html',
    {'form': form, 'method': 'edit', 'id': comment.id})