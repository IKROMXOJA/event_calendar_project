from django.contrib import admin
from .models import Event

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'start_date', 'end_date', 'user', 'team', 'is_active')
    search_fields = ('title', 'description', 'user__username', 'team__name')
    list_filter = ('team', 'start_date', 'is_active')
    ordering = ('-start_date',)
    list_editable = ('is_active',)  # admin orqali faollikni bevosita o‘zgartirish
    date_hierarchy = 'start_date'   # tepasida sana bo‘yicha filtrlash
    readonly_fields = ('id',)       # id ni faqat o‘qish rejimida ko‘rsatadi
