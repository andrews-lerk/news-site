from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.contrib.auth.models import User
from django.db.models import *
from django.urls import reverse

user = User

# Create your models here.
class Tag(models.Model):

    tag = models.CharField(max_length=255, verbose_name='tag_name')
    slug = models.SlugField(max_length=255, null=True, verbose_name='catURL')

    def __str__(self):
        return self.tag

    def get_absolute_url(self):
        return reverse('cat_view', kwargs={'cat_slug': self.slug})

class NewPost(models.Model):

    title = models.CharField(max_length=255, verbose_name='title')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')
    text = models.TextField()
    img = models.ImageField(null=True)
    pub_date = models.DateTimeField(auto_now=False, auto_now_add=False)
    comments = GenericRelation('Comment')
    cat = models.ManyToManyField(Tag, verbose_name='tag', related_name='get_posts')
    count = PositiveIntegerField(default=0)

    @property
    def tag(self):
        return self.cat.objects.all()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('personal_new', kwargs={'post_slug': self.slug})

class Comment(models.Model):

    auth_user = models.ForeignKey(user, verbose_name='author', on_delete=models.CASCADE)
    date = models.DateField(auto_now=True)
    text = models.TextField()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()

    def get_absolute_url(self):
        return reverse('delete_comment', kwargs={'comment_id': self.pk})

    def __str__(self):
        return f'comment by {self.auth_user}'

class UserQuestion(models.Model):

    user_name = models.CharField(max_length=255)
    text = models.TextField()

    def __str__(self):
        return f'Question by {self.user_name}'

class Applications(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    file = models.FileField(null=True)

    def get_absolute_url(self):
        return reverse('download', kwargs={'file_id': self.pk})

    def __str__(self):
        return f'Application {self.title}'

class Resume(models.Model):
    file = models.FileField()

    def __str__(self):
        return f'Resume {self.file}'