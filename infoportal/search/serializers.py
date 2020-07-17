from rest_framework import serializers

from .models import Search, AutoCompletion, SearchOptions


class SearchSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Search
        fields = ['search_text', 'search_options', 'page_size']


class SearchHistorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Search
        fields = ['search', 'userid']


class AutoCompletionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = AutoCompletion
        fields = ['search_text', 'page_size']


class SearchOptionsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SearchOptions
        fields = ['document_type',
                  'brief_document_description',
                  'name_ru',
                  'name_en',
                  'abstract',
                  'note',
                  'full_designation_of_the_document',
                  'document_status',
                  'document_approval_date',
                  'date_of_adoption',
                  'effective_date',
                  'recover_date',
                  'okved',
                  'oks',
                  'tk',
                  'mtk',
                  'keywords'
                  ]
