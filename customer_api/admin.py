from django.contrib import admin
from .models import Customer, ChatRecord


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('real_name', 'phone')
    search_fields = ('real_name', 'phone')

@admin.register(ChatRecord)
class ChatRecordAdmin(admin.ModelAdmin):
    list_display = ('customer', 'role', 'content', 'created_at')
    list_filter = ('role', 'created_at')
    search_fields = ('customer__real_name', 'content')

