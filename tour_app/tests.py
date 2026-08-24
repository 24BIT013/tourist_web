from unittest.mock import patch
from urllib.parse import parse_qs

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

    @patch('tour_app.views.urlopen')
    @override_settings(
        MIDDLEWARE=[
            middleware
            for middleware in settings.MIDDLEWARE
            if middleware != 'whitenoise.middleware.WhiteNoiseMiddleware'
        ]
    )
    def test_booking_sends_notification_and_returns_to_the_site(self, mock_urlopen):
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

        self.assertRedirects(response, reverse('home'), fetch_redirect_response=False)
        mock_urlopen.assert_called_once()
        notification_request = mock_urlopen.call_args.args[0]
        self.assertEqual(notification_request.full_url, settings.BOOKING_NOTIFICATION_URL)
        notification_data = parse_qs(notification_request.data.decode('utf-8'))
        self.assertEqual(notification_data['Customer name'], ['Amina Ali'])
        self.assertEqual(notification_data['Customer email'], ['amina@example.com'])
        self.assertEqual(notification_data['Package'], ['Zanzibar Escape'])
        self.assertEqual(notification_data['Special requests'], ['Airport pickup'])

    @patch('tour_app.views.urlopen', side_effect=ConnectionError('FormSubmit unavailable'))
    @override_settings(
        MIDDLEWARE=[
            middleware
            for middleware in settings.MIDDLEWARE
            if middleware != 'whitenoise.middleware.WhiteNoiseMiddleware'
        ]
    )
    def test_booking_returns_to_site_when_notification_delivery_fails(self, mock_urlopen):
        with self.assertLogs('tour_app.views', level='ERROR'):
            response = self.client.post(reverse('home'), {
                'guest_name': 'Amina Ali',
                'guest_email': 'amina@example.com',
                'package': self.package.pk,
                'travelers': 2,
                'contact_method': 'whatsapp',
            })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('home'))
        mock_urlopen.assert_called_once()
