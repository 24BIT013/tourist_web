from django.conf import settings



def site_settings(request):
    whatsapp_phone_number = getattr(settings, 'WHATSAPP_PHONE_NUMBER', '0612001424')
    normalized_whatsapp_phone = ''.join(ch for ch in str(whatsapp_phone_number) if ch.isdigit())

    return {
        'whatsapp_phone_number': normalized_whatsapp_phone,
        'contact_email': getattr(settings, 'CONTACT_EMAIL', 'burminho098@gmail.com'),
        'whatsapp_default_message': getattr(
            settings,
            'WHATSAPP_DEFAULT_MESSAGE',
            'Hello, I would like more information about your travel packages.',
        ),
    }
