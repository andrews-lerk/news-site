from functools import wraps
from django.db.models import F
from django.db import transaction

from .models import NewPost


def counted(f):
    """ decorator for count news """
    @wraps(f)
    def decorator(request, *args, **kwargs):
        with transaction.atomic():
            counter, created = NewPost.objects.get_or_create(slug=request.path.split('/')[-2])
            counter.count = F('count') + 1
            counter.save()
        return f(request, *args, **kwargs)
    return decorator