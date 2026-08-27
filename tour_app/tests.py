from unittest.mock import patch
from urllib.parse import parse_qs

from django.conf import settings
from django.test import TestCase
from django.test import override_settings
from django.urls import reverse

from .models import Booking, Destination, TourPackage


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
        SECURE_SSL_REDIRECT=False,
        MIDDLEWARE=[
            middleware
            for middleware in settings.MIDDLEWARE
            if middleware != 'whitenoise.middleware.WhiteNoiseMiddleware'
        ]
    )
    def test_booking_sends_notification_and_returns_to_the_site(self, mock_urlopen):
        mock_urlopen.return_value.__enter__.return_value.status = 200
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

        self.assertRedirects(response, f'{reverse("home")}?booking=success#booking', fetch_redirect_response=False)
        mock_urlopen.assert_called_once()
        notification_request = mock_urlopen.call_args.args[0]
        self.assertEqual(notification_request.full_url, settings.BOOKING_NOTIFICATION_URL)
        notification_data = parse_qs(notification_request.data.decode('utf-8'))
        self.assertEqual(notification_data['Customer name'], ['Amina Ali'])
        self.assertEqual(notification_data['Customer email'], ['amina@example.com'])
        self.assertEqual(notification_data['email'], ['amina@example.com'])
        self.assertEqual(notification_data['Package'], ['Zanzibar Escape'])
        self.assertEqual(notification_data['Estimated total'], ['$1,000'])
        self.assertEqual(notification_data['Special requests'], ['Airport pickup'])
        self.assertEqual(notification_data['_next'], ['https://touristwebs.vercel.app/'])
        self.assertEqual(Booking.objects.get().total_price, '$1,000')

    @patch('tour_app.views.urlopen', side_effect=ConnectionError('FormSubmit unavailable'))
    @override_settings(
        SECURE_SSL_REDIRECT=False,
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
        self.assertEqual(response.url, f'{reverse("home")}?booking=saved#booking')
        mock_urlopen.assert_called_once()


@override_settings(
    SECURE_SSL_REDIRECT=False,
    MIDDLEWARE=[
        middleware
        for middleware in settings.MIDDLEWARE
        if middleware != 'whitenoise.middleware.WhiteNoiseMiddleware'
    ]
)
class DestinationManagementTests(TestCase):
    def setUp(self):
        self.staff_user = self._create_staff_user()

    def _create_staff_user(self):
        from django.contrib.auth import get_user_model
        return get_user_model().objects.create_user('manager', password='password', is_staff=True)

    def test_staff_can_create_and_edit_a_destination(self):
        self.client.force_login(self.staff_user)
        response = self.client.post(reverse('destination_create'), {
            'name': 'Serengeti',
            'country': 'Tanzania',
            'description': 'Wildlife and vast plains.',
            'image_url': 'https://example.com/serengeti.jpg',
        })
        self.assertRedirects(response, reverse('dashboard'), fetch_redirect_response=False)
        destination = Destination.objects.get(name='Serengeti')

        response = self.client.post(reverse('destination_edit', args=[destination.pk]), {
            'name': 'Serengeti National Park',
            'country': 'Tanzania',
            'description': 'Wildlife safaris.',
            'image_url': 'https://example.com/serengeti.jpg',
        })
        self.assertRedirects(response, reverse('dashboard'), fetch_redirect_response=False)
        destination.refresh_from_db()
        self.assertEqual(destination.name, 'Serengeti National Park')


class AdminSiteTests(TestCase):
    def test_site_models_are_registered_with_admin(self):
        from django.contrib import admin

        self.assertIn(Destination, admin.site._registry)
        self.assertIn(TourPackage, admin.site._registry)
        self.assertIn(Booking, admin.site._registry)
