from django.contrib import admin
from .models import Account,FriendRequest

class AuthorAdmin(admin.ModelAdmin):
    pass
admin.site.register(Account, AuthorAdmin)
admin.site.register(FriendRequest,AuthorAdmin)


