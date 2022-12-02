from django.contrib import admin

from apps.post.models import Post, PostImage, Save


admin.site.register(Post)
admin.site.register(PostImage)
admin.site.register(Save)