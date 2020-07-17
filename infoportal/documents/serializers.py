from rest_framework import serializers

from drf_writable_nested.serializers import WritableNestedModelSerializer

from . import models


class CISCountriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CISCountries
        fields = '__all__'


class CodeOKVEDSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CodeOKVED
        fields = '__all__'


class CodeOKSSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CodeOKS
        fields = '__all__'


class CodeOKPDSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CodeOKPD
        fields = '__all__'


class OriginLanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.OriginLanguage
        fields = '__all__'


class RelatedDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Documents
        fields = ('id', 'doc_name_ru')


class DocumentsSerializer(serializers.ModelSerializer):
    classifier_enterd_countries = CISCountriesSerializer(many=True, required=False)
    classifier_okved = CodeOKVEDSerializer(many=True)
    classifier_oks = CodeOKSSerializer(many=True, required=False)
    classifier_okp = CodeOKPDSerializer(many=True, required=False)
    doc_origin_language = OriginLanguageSerializer(many=True)
    related_documents = RelatedDocumentSerializer(many=True, required=False)

    class Meta:
        model = models.Documents
        exclude = ('doc_html_content',
                   'doc_image_content',
                   'doc_pdf_content')


class ShortDocumentsSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Documents
        exclude = ('doc_name_en',
                   'doc_annotation',
                   'doc_sys_number',
                   'doc_full_mark',
                   'application_status',
                   'doc_limit_date',
                   'doc_on_rf_use',
                   'classifier_pns',
                   'doc_assign_org',
                   'classifier_enterd_countries',
                   'doc_reg_text',
                   'doc_enter_org',
                   'classifier_okved',
                   'classifier_oks',
                   'classifier_okp',
                   'tk_rus',
                   'org_author_name',
                   'mtk_dev',
                   'keywords',
                   'doc_annotation_ru',
                   'doc_origin_language',
                   'contains_in_npa_links',
                   'doc_o_zsh',
                   'doc_o_zgo_vch',
                   'doc_o_zgo',
                   'doc_o_zsh_vch',
                   'doc_supplemented',
                   'doc_supplementing',
                   'related_documents',
                   'doc_outside_system',
                   'image_contemt_name',
                   'pdf_content_name',
                   'doc_html_content',
                   'doc_image_content',
                   'doc_pdf_content',
                   'doc_changes',
                   'has_document_case')


class DocumentsListSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Documents
        fields = ('id', 'doc_mark', 'doc_name_ru', 'doc_status')


class TextSettingsSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.TextSetings
        fields = '__all__'


class PositionSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Position
        exclude = ('id', )


class CommentsSerializer(WritableNestedModelSerializer):
    position = PositionSerializer()

    class Meta:
        model = models.Comments
        fields = '__all__'


class DocumentsNoticeSerializer(serializers.ModelSerializer):
    text_settings = TextSettingsSerializer(many=True, read_only=True)
    comments = CommentsSerializer(many=True, read_only=True)

    class Meta:
        model = models.DocumentsNotice
        exclude = ('user', 'document')


class RateDocumentsSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Ratings
        fields = '__all__'
