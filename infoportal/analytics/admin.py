from django.contrib import admin
from .models import *


class AnalyticsAdmin(admin.ModelAdmin):
    list_display = ('date', 'documents', 'users', 'companies', 'notes')


class DocumentsAnalyticsAdmin(admin.ModelAdmin):
    list_display = (
        'date',
        'total_docs',
        'russian_docs',
        'foreign_docs',
        'gost_r',
        'pnst',
        'gost',
        'pr',
        'r',
        'pmg',
        'rmg',
        'its',
        'ok',
        'sp',
        'iso',
        'mek'
    )


admin.site.register(Analytics, AnalyticsAdmin)
admin.site.register(DocumentsAnalytics, DocumentsAnalyticsAdmin)
