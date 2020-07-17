from django.contrib import admin

from .models import Notes, Comments


class NotesAdmin(admin.ModelAdmin):
    model = Notes
    list_display = ('id', )
    search_fields = ('id', )


class CommentsAdmin(admin.ModelAdmin):
    model = Comments
    list_display = ('id', )
    search_fields = ('id', )


admin.site.register(Notes, NotesAdmin)
admin.site.register(Comments, CommentsAdmin)
