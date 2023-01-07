from django.contrib import admin

from apps.post.models import Post, PostImage, Save, Like


admin.site.register(Post)
admin.site.register(PostImage)
admin.site.register(Save)
admin.site.register(Like)