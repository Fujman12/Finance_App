from django.contrib import admin
from .models import inputDB

@admin.register(inputDB)
class AuthorAdmin(admin.ModelAdmin):
    fields = ('id', 'title', 'date_created', 'date_modified', 'user', 'data')
    list_display = ('id', 'title', 'date_created', 'date_modified', 'user')

    readonly_fields = ('id', 'data')