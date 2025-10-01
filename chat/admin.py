from django.contrib import admin
from .models import Conversation, Message
# Register your models here.

class ConversationsAdmin(admin.ModelAdmin):
    list_filter = ['id']
    list_display = ['id', 'created_at']

class MessageAdmin(admin.ModelAdmin):
    list_filter = ['conversation']
    list_display = ['conversation', 'question', 'answer', 'created_at']

admin.site.register(Conversation, ConversationsAdmin)
admin.site.register(Message, MessageAdmin)