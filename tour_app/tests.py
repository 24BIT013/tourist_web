from unittest.mock import patch

from django.conf import settings
from django.test import TestCase
from django.test import override_settings
from django.urls import reverse

from .models import TourPackage


class BookingNotificationTests(TestCase):
    def setUp(self):
        self.package = TourPackage.objects.create(
            title='Zanzibar Escape',
            slug='zanzibar-escape',
            country='Tanzania',
            duration='4 days',
            price='$500',
        )

    @patch('tour_app.views.send_mail')
    @override_settings(
        MIDDLEWARE=[
            middleware
            for middleware in settings.MIDDLEWARE
            if middleware != 'whitenoise.middleware.WhiteNoiseMiddleware'
        ]
    )
    def test_booking_sends_email_and_opens_whatsapp_with_details(self, mock_send_mail):
        response = self.client.post(reverse('home'), {
            'guest_name': 'Amina Ali',
            'guest_email': 'amina@example.com',
            'guest_phone': '+255 700 000 000',
            'whatsapp_number': '+255 711 111 111',
            'package': self.package.pk,
            'travelers': 2,
            'start_date': '2026-10-01',
            'return_date': '2026-10-05',
            'contact_method': 'whatsapp',
            'special_requests': 'Airport pickup',
        })

        self.assertRedirects(response, response.url, fetch_redirect_response=False)
        self.assertTrue(response.url.startswith('https://wa.me/255612001424?'))
        self.assertIn('Amina+Ali', response.url)
        self.assertIn('Zanzibar+Escape', response.url)
        mock_send_mail.assert_called_once()
        self.assertEqual(mock_send_mail.call_args.kwargs['recipient_list'], ['wordoxw@gmail.com'])
        self.assertIn('Airport pickup', mock_send_mail.call_args.kwargs['message'])

    @patch('tour_app.views.send_mail', side_effect=ConnectionError('SMTP unavailable'))
    @override_settings(
        MIDDLEWARE=[
            middleware
            for middleware in settings.MIDDLEWARE
            if middleware != 'whitenoise.middleware.WhiteNoiseMiddleware'
        ]
    )
    def test_booking_still_opens_whatsapp_when_email_delivery_fails(self, mock_send_mail):
        with self.assertLogs('tour_app.views', level='ERROR'):
            response = self.client.post(reverse('home'), {
                'guest_name': 'Amina Ali',
                'guest_email': 'amina@example.com',
                'package': self.package.pk,
                'travelers': 2,
                'contact_method': 'whatsapp',
            })

        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('https://wa.me/255612001424?'))
        mock_send_mail.assert_called_once()
