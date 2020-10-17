from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.urls import reverse
from ckeditor.fields import RichTextField
from django.utils.text import slugify
from django.utils.crypto import get_random_string


class Query(models.Model):
    CATEGORY = [('Mental Health', 'Mental Health'),
                ('Physical Health', 'Physical Health'),
                ('Experience', 'Experience'),
                ('Post Covid-19', 'Post Covid-19')]

    title = models.CharField(max_length=240)
    user = models.ForeignKey(get_user_model(),
                             null=True,
                             on_delete=models.SET_NULL)
    content = RichTextField(null=True, blank=True)
    likes = models.ManyToManyField(User,
                                   default=None,
                                   blank=True,
                                   related_name="query_likes")
    category = models.CharField(max_length=30, choices=CATEGORY, default='GEN')
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    slug = models.SlugField(null=True, unique=True, max_length=256)

    # shows up in admin panel instead of just plain numbers
    # applies elsewhere in the project too
    def __str__(self):
        return self.title

    # helps display a different text depending on whether a person
    # has liked a post or not. Re: forum/query_detail.html; request.user.id
    # in this list.
    def likes_as_flat_user_id_list(self):
        return self.likes.values_list('id', flat=True)

    # slug for the post; applies elsewhere in the project too
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    # absolute_url/ fallback url as I call it. Using the slug as a key-word
    # arg we made earlier while slugifying the title of the post.
    def get_absolute_url(self):
        return reverse('forum:detail', kwargs={'slug': self.slug})


class Answer(models.Model):
    user = models.ForeignKey(get_user_model(),
                             null=True,
                             on_delete=models.SET_NULL)
    query = models.ForeignKey(Query, on_delete=models.CASCADE)
    content = RichTextField()
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(User,
                                   default=None,
                                   blank=True,
                                   related_name="answer_likes")
    slug = models.SlugField(null=True, unique=True, max_length=256)
    isaccepted = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        uniqueid = get_random_string(length=8)
        self.slug = slugify(uniqueid)
        super().save(*args, **kwargs)

    """
    self.query.slug exists so the answer falls back to the slug of the query
    upon submitting a form. How? Re: forum/query_detail.html
    (edit option in there)
    to answer the query, only query.slug is used. generic stuff,
    no explanation req. Ask DomeCode Discord for help on this if needed.
    Notice the use of query.slug and answer.slug to go edit an answer.
    However, the fallback url still remains self.query.slug given we want
    to come back to the original query after submitting something.
    """

    def get_absolute_url(self):
        return reverse('forum:detail', kwargs={'slug': self.query.slug})


class Comment(models.Model):
    user = models.ForeignKey(get_user_model(),
                             null=True,
                             on_delete=models.SET_NULL)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    content = RichTextField()
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    slug = models.SlugField(null=True, unique=False, max_length=256)
    """
    self.answer.query.slug exists so the answer falls back to the slug of the
    query
    upon submitting a form. How? Re: forum/answer_detail.html
    (edit option in there -> for comments)
    to comment on the answer, only query.slug and answer.slug is used.
    generic stuff,
    no explanation req. Ask DomeCode Discord for help on this if needed.
    Notice the use of query.slug, answer.slug and comment.slug to go edit an
    answer.
    However, the fallback url still remains self.answer.query.slug given
    we want
    to come back to the original query after submitting something.
    """
    """
    todo - redirect to answer view instead of question view, pass multiple
    kwargs.slug and possibly answer slug as aslug. make respective changes
    in urls.py too
    """

    def get_absolute_url(self):
        return reverse('forum:detail', kwargs={'slug': self.answer.query.slug})

    def save(self, *args, **kwargs):
        uniqueid = get_random_string(length=8)
        self.slug = slugify(uniqueid)
        super().save(*args, **kwargs)
