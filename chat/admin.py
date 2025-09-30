from django.contrib import admin
from .models import MessageThread, Message

# Register your models here.


from django.contrib import admin
from .models import MessageThread, Message

@admin.register(MessageThread)
class MessageThreadAdmin(admin.ModelAdmin):
    list_display = ('ad', 'buyer', 'seller', 'created_at')

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('thread', 'sender', 'text', 'is_read', 'created_at')
