from django.urls import path
from .views import (
    ContactListCreateView, ContactDetailView, ContactSearchView, 
    ContactImportView, ContactExportCSVView, ContactExportVCardView,
)

urlpatterns = [
    path('', ContactListCreateView.as_view(), name='contacts-list-create'),
    path('<int:pk>/', ContactDetailView.as_view(), name='contacts-detail'),
    path('search/', ContactSearchView.as_view(), name='contacts-search'),
     path('import/', ContactImportView.as_view(), name='contacts-import'),
    path('export/csv/', ContactExportCSVView.as_view(), name='contacts-export-csv'),
    path('<int:pk>/export/vcard/', ContactExportVCardView.as_view(), name='contacts-export-vcard'),
]
