from rest_framework import views
from rest_framework.response import Response

from documents.models import Documents

from .lib import diff_files


class CompareHTML(views.APIView):

    def get(self, request):
        document_1_id = self.request.query_params.get('doc1')
        document_2_id = self.request.query_params.get('doc2')
 
        doc_html_1 = Documents.objects.get(id=document_1_id)
        doc_html_2 = Documents.objects.get(id=document_2_id)
        
        htmldiff = diff_files(doc_html_1.doc_html_content,
                              doc_html_2.doc_html_content,
                              True)
        data = {"file": htmldiff}
        return Response(data)
