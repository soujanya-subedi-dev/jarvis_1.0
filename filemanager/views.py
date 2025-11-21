from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import File
from .serializers import FileSerializer
from rest_framework.parsers import MultiPartParser, FormParser

class FileListCreateView(generics.ListCreateAPIView):
    serializer_class = FileSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def get_queryset(self):
        return File.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        file_obj = serializer.validated_data['file']
        # Auto-assign category based on file type
        ext = file_obj.name.split('.')[-1].lower()
        category = 'other'
        if ext in ['jpg','jpeg','png','gif','bmp']:
            category = 'image'
        elif ext in ['pdf','doc','docx','txt','ppt','pptx','xls','xlsx']:
            category = 'document'
        elif ext in ['mp4','mov','avi','mkv']:
            category = 'video'
        elif ext in ['mp3','wav','aac']:
            category = 'audio'
        elif ext in ['py','js','html','css','java','c','cpp']:
            category = 'code'
        serializer.save(user=self.request.user, category=category, name=file_obj.name)


class FileDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = FileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return File.objects.filter(user=self.request.user)
