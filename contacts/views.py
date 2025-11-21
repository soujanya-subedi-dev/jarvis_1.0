from django.shortcuts import render

# Create your views here.
from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Contact
from .serializers import ContactSerializer
from django.db.models import Q

# List + Create
class ContactListCreateView(generics.ListCreateAPIView):
    serializer_class = ContactSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Contact.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# Retrieve + Update + Delete
class ContactDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ContactSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Contact.objects.filter(user=self.request.user)


# Search Contacts
class ContactSearchView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        q = request.query_params.get('q', '')

        queryset = Contact.objects.filter(
            user=request.user
        ).filter(
            Q(first_name__icontains=q) |
            Q(last_name__icontains=q) |
            Q(phone__icontains=q) |
            Q(email__icontains=q)
        )

        serializer = ContactSerializer(queryset, many=True)
        return Response(serializer.data)


# contacts/views.py (append)
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from django.http import HttpResponse
from .utils import parse_contacts_csv, contacts_to_csv, contact_to_vcard

class ContactImportView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        """
        Expect multipart/form-data with a file field named 'file'
        """
        uploaded = request.FILES.get('file')
        if not uploaded:
            return Response({"detail": "No file uploaded. Use form field 'file'."},
                            status=status.HTTP_400_BAD_REQUEST)
        created, errors = parse_contacts_csv(uploaded, request.user)
        return Response({"created": created, "errors": errors}, status=status.HTTP_201_CREATED)


class ContactExportCSVView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        queryset = Contact.objects.filter(user=request.user)
        csv_text, filename = contacts_to_csv(queryset)
        response = HttpResponse(csv_text, content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response


class ContactExportVCardView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        try:
            contact = Contact.objects.get(pk=pk, user=request.user)
        except Contact.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        vcard_text = contact_to_vcard(contact)
        response = HttpResponse(vcard_text, content_type='text/vcard')
        response['Content-Disposition'] = f'attachment; filename="contact_{contact.id}.vcf"'
        return response
