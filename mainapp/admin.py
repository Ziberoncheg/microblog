from django.contrib import admin
from mainapp.models import Post, Post_comments
# Register your models here.
admin.site.register(Post)
admin.site.register(Post_comments)