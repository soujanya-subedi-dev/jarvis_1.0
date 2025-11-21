# contacts/utils.py
import csv
from io import StringIO
from .models import Contact

def parse_contacts_csv(fileobj, user):
    """
    fileobj is an uploaded file (InMemoryUploadedFile) from request.FILES['file']
    Returns (created_count, errors_list)
    """
    errors = []
    created = 0

    # Read text
    content = fileobj.read().decode('utf-8-sig')
    f = StringIO(content)
    reader = csv.DictReader(f)
    required_fields = ('first_name',)

    for i, row in enumerate(reader, start=1):
        if not row.get('first_name'):
            errors.append(f"Row {i}: missing first_name")
            continue

        try:
            Contact.objects.create(
                user=user,
                first_name=row.get('first_name', '').strip(),
                last_name=row.get('last_name') or None,
                phone=row.get('phone') or None,
                email=row.get('email') or None,
                address=row.get('address') or None,
                notes=row.get('notes') or None,
            )
            created += 1
        except Exception as e:
            errors.append(f"Row {i}: {str(e)}")

    return created, errors


def contacts_to_csv(contacts_qs):
    """
    contacts_qs: queryset of Contact
    returns: (csv_text, filename)
    """
    f = StringIO()
    fieldnames = ['first_name','last_name','phone','email','address','notes','created_at']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    for c in contacts_qs:
        writer.writerow({
            'first_name': c.first_name,
            'last_name': c.last_name or '',
            'phone': c.phone or '',
            'email': c.email or '',
            'address': c.address or '',
            'notes': c.notes or '',
            'created_at': c.created_at.isoformat(),
        })
    filename = 'contacts_export.csv'
    return f.getvalue(), filename


def contact_to_vcard(contact):
    """
    Very small vCard builder (vCard 3.0 minimal)
    """
    lines = [
        "BEGIN:VCARD",
        "VERSION:3.0",
        f"N:{contact.last_name or ''};{contact.first_name}",
        f"FN:{contact.first_name} {contact.last_name or ''}".strip(),
    ]
    if contact.email:
        lines.append(f"EMAIL;TYPE=INTERNET:{contact.email}")
    if contact.phone:
        lines.append(f"TEL;TYPE=CELL:{contact.phone}")
    if contact.address:
        # vCard ADR format is complicated; put full address in LABEL
        lines.append(f"ADR;TYPE=HOME:;;{contact.address.replace(';',',')}")
    if contact.notes:
        lines.append(f"NOTE:{contact.notes}")
    lines.append("END:VCARD")
    return "\r\n".join(lines)
