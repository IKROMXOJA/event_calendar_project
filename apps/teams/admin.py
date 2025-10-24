from django.contrib import admin
from .models import Team

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'admin', 'created_at')
    search_fields = ('name', 'admin__username')
    filter_horizontal = ('members',)
