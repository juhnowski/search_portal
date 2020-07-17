from django.contrib import admin

from .models import Search, AutoCompletion, SearchOptions, SearchHistory


class SearchAdmin(admin.ModelAdmin):
    model = Search
    list_display = ('id', 'search_text', 'search_options', 'page_size')
    search_fields = ('user', 'search_text', 'search_options', 'page_size')


class SearchHistoryAdmin(admin.ModelAdmin):
    model = Search
    list_display = ('search', 'userid')
    search_fields = ('search', 'userid')


class AutoCompletionAdmin(admin.ModelAdmin):
    model = AutoCompletion
    list_display = ('id', 'search_text', 'page_size')
    search_fields = ('id', 'search_text', 'page_size')

class SearchOptionsAdmin(admin.ModelAdmin):
    model = SearchOptions
    list_display = ('document_type', 'brief_document_description', 'name_ru', 'name_en', 'abstract', 'note', 'full_designation_of_the_document', 'document_status', \
    'document_approval_date', 'date_of_adoption', 'effective_date', 'recover_date', 'okved', 'oks', 'tk', 'mtk', 'keywords', )
    search_fields = ('document_type', 'brief_document_description', 'name_ru', 'name_en', 'abstract', 'note', 'full_designation_of_the_document', 'document_status', \
    'document_approval_date', 'date_of_adoption', 'effective_date', 'recover_date', 'okved', 'oks', 'tk', 'mtk', 'keywords', )


admin.site.register(Search, SearchAdmin)
admin.site.register(AutoCompletion, AutoCompletionAdmin)
admin.site.register(SearchOptions, SearchOptionsAdmin)
admin.site.register(SearchHistory, SearchHistoryAdmin)
