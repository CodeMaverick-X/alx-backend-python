from django.contrib import admin
from .models import  Message, User, Conversation

# Register your models here.

admin.site.register(Message)
admin.site.register(User)
admin.site.register(Conversation)

