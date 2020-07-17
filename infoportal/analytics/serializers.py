from django.contrib.auth import get_user_model

from rest_framework import serializers

from documents.models import Documents
from notes.models import Notes
from users.models import Company

from .models import *


class DocumentAnalyticsModelSerializer(serializers.ModelSerializer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['labels'] = serializers.SerializerMethodField()

    def get_labels(self, *args):
        labels = {}

        for field in self.Meta.model._meta.get_fields():
            if field.name in self.fields:
                labels[field.name] = field.verbose_name

        return labels

    class Meta:
        model = DocumentsAnalytics
        exclude = ('id', 'date')


class AnalyticsSerializer(serializers.ModelSerializer):
    documents = DocumentAnalyticsModelSerializer(read_only=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['labels'] = serializers.SerializerMethodField()

    def get_labels(self, *args):
        labels = {}

        for field in self.Meta.model._meta.get_fields():
            if field.name in self.fields:
                labels[field.name] = field.verbose_name

        return labels

    class Meta:
        model = Analytics
        exclude = ('id', )


class DocumentsAnalyticsSerializer(serializers.ModelSerializer):
    documents = DocumentAnalyticsModelSerializer(read_only=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['labels'] = serializers.SerializerMethodField()

    def get_labels(self, *args):
        labels = {}

        for field in self.Meta.model._meta.get_fields():
            if field.name in self.fields:
                labels[field.name] = field.verbose_name

        return labels

    class Meta:
        model = Analytics
        fields = ('date', 'documents')


class UsersAnalyticsSerializer(serializers.ModelSerializer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['labels'] = serializers.SerializerMethodField()

    def get_labels(self, *args):
        labels = {}

        for field in self.Meta.model._meta.get_fields():
            if field.name in self.fields:
                labels[field.name] = field.verbose_name

        return labels

    class Meta:
        model = Analytics
        fields = ('date', 'users')


class CompaniesAnalyticsSerializer(serializers.ModelSerializer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['labels'] = serializers.SerializerMethodField()

    def get_labels(self, *args):
        labels = {}

        for field in self.Meta.model._meta.get_fields():
            if field.name in self.fields:
                labels[field.name] = field.verbose_name

        return labels

    class Meta:
        model = Analytics
        fields = ('date', 'companies')


class NotesAnalyticsSerializer(serializers.ModelSerializer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['labels'] = serializers.SerializerMethodField()

    def get_labels(self, *args):
        labels = {}

        for field in self.Meta.model._meta.get_fields():
            if field.name in self.fields:
                labels[field.name] = field.verbose_name

        return labels

    class Meta:
        model = Analytics
        fields = ('date', 'notes')


class CreateNewAnalyticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Analytics
        fields = '__all__'

    def create(self, *args, **kwargs):
        try:
            user_model = get_user_model()

            documents_total = Documents.objects.filter().count()
            gost_r = Documents.objects.filter(doc_kind='ГОСТ Р').count()
            pnst = Documents.objects.filter(doc_kind='ПНСТ').count()
            gost = Documents.objects.filter(doc_kind='ГОСТ').count()
            pr = Documents.objects.filter(doc_kind='ПР').count()
            r = Documents.objects.filter(doc_kind='Р').count()
            pmg = Documents.objects.filter(doc_kind='ПМГ').count()
            rmg = Documents.objects.filter(doc_kind='РМГ').count()
            its = Documents.objects.filter(doc_kind='ИТС').count()
            ok = Documents.objects.filter(doc_kind='ОК').count()
            sp = Documents.objects.filter(doc_kind='СП').count()
            iso = Documents.objects.filter(doc_kind='ИСО').count()
            mek = Documents.objects.filter(doc_kind='МЭК').count()

            documents = DocumentsAnalytics.objects.create(
                total_docs=documents_total,
                gost_r=gost_r,
                pnst=pnst,
                gost=gost,
                pr=pr,
                r=r,
                pmg=pmg,
                rmg=rmg,
                its=its,
                ok=ok,
                sp=sp,
                iso=iso,
                mek=mek,
                russian_docs=(gost_r + pnst + gost + pr + r + pmg + rmg + its + ok + sp),
                foreign_docs=(iso + mek)
            )

            users = user_model.objects.filter().count()
            companies = Company.objects.filter().count()
            notes = Notes.objects.filter().count()

            Analytics.objects.create(
                documents=documents,
                users=users,
                companies=companies,
                notes=notes
            )
            return True

        except:
            return False
