from django.contrib import admin

from .models import JournalRecord


class JournalAdmin(admin.ModelAdmin):
    model = JournalRecord
    list_display = ('type', 'level', 'message')


admin.site.register(JournalRecord, JournalAdmin)
