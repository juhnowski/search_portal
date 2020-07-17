from django.contrib import admin

from .models import Documents, CISCountries, CodeOKVED, CodeOKS, \
    CodeOKPD, OriginLanguage, TextSetings, Comments, DocumentsNotice, \
    Position, Ratings


class DocumentsAdmin(admin.ModelAdmin):
    model = Documents
    list_display = ('doc_name_ru', 'doc_status', 'doc_rating')
    list_filter = ('doc_name_ru', 'doc_status')
    search_fields = ('doc_name_ru', )


class CISCountriesAdmin(admin.ModelAdmin):
    model = CISCountries
    list_display = ('name', )
    search_fields = ('name', )


class CodeOKVEDAdmin(admin.ModelAdmin):
    model = CodeOKVED
    list_display = ('code', 'title')
    search_fields = ('code', )


class CodeOKSAdmin(admin.ModelAdmin):
    model = CodeOKS
    list_display = ('code', 'title')
    search_fields = ('code', )


class CodeOKPDAdmin(admin.ModelAdmin):
    model = CodeOKPD
    list_display = ('code', 'title')
    search_fields = ('code', )


class OriginLanguageAdmin(admin.ModelAdmin):
    model = OriginLanguage
    list_display = ('language', )
    search_fields = ('language', )


class TextSetingsAdmin(admin.ModelAdmin):
    model = TextSetings
    list_display = ('id', 'position')
    search_fields = ('id', )


class CommentsAdmin(admin.ModelAdmin):
    model = Comments
    list_display = ('id', 'elem')
    search_fields = ('id', )


class DocumentsNoticeAdmin(admin.ModelAdmin):
    model = DocumentsNotice
    list_display = ('id', 'user')
    search_fields = ('user', )


class PositionAdmin(admin.ModelAdmin):
    model = Position
    list_display = ('id', )


class RatingsAdmin(admin.ModelAdmin):
    model = Ratings
    list_display = ('value', 'document', 'user')


admin.site.register(Documents, DocumentsAdmin)
admin.site.register(CISCountries, CISCountriesAdmin)
admin.site.register(CodeOKVED, CodeOKVEDAdmin)
admin.site.register(CodeOKS, CodeOKSAdmin)
admin.site.register(CodeOKPD, CodeOKPDAdmin)
admin.site.register(OriginLanguage, OriginLanguageAdmin)
admin.site.register(TextSetings, TextSetingsAdmin)
admin.site.register(Comments, CommentsAdmin)
admin.site.register(DocumentsNotice, DocumentsNoticeAdmin)
admin.site.register(Position, PositionAdmin)
admin.site.register(Ratings, RatingsAdmin)
