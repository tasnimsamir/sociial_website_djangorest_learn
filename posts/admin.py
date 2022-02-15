from django.contrib import admin
from .models import Post, Comments, Like

class AuthorAdmin(admin.ModelAdmin):
    pass
admin.site.register(Post, AuthorAdmin)
admin.site.register(Comments, AuthorAdmin)
admin.site.register(Like, AuthorAdmin)


