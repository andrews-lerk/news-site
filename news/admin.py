from django.contrib import admin
from .models import *

# Register your models here.

class NewPostAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug":("title",)}

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug":("tag",)}

admin.site.register(NewPost, NewPostAdmin)
admin.site.register(Comment)
admin.site.register(Tag, CategoryAdmin)
admin.site.register(UserQuestion)
admin.site.register(Applications)
admin.site.register(Resume)