import datetime
import json
from unittest.mock import patch, MagicMock
from django.test import TestCase, RequestFactory
from .views import get_usd_to_eur_rate

class ExchangeRateTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

    @patch('backendChallenge.views.get_or_create_exchange_rate')
    def test_get_usd_to_eur_rate_current_date(self, mock_get_or_create_exchange_rate):
        mock_get_or_create_exchange_rate.return_value = 1.2

        request = self.factory.get('/')
        response = get_usd_to_eur_rate(request)


        self.assertEqual(response.status_code, 200)

        response_data = json.loads(response.content)

        self.assertIn('usd_to_eur', response_data)
        self.assertAlmostEqual(response_data['usd_to_eur'], 1.2, places=2)

    @patch('backendChallenge.views.get_or_create_exchange_rate')
    @patch('backendChallenge.views.ExchangeRate.objects.filter')
    def test_get_usd_to_eur_rate_date_range(self, mock_filter, mock_get_or_create_exchange_rate):
        mock_get_or_create_exchange_rate.side_effect = lambda date: 1.1 if date == datetime.date(2023, 1, 1) else 1.3
        mock_filter.return_value.aggregate.return_value = {'rate__avg': 1.2}

        request = self.factory.get('/', {'start_date': '2023-01-01', 'end_date': '2023-01-05'})
        response = get_usd_to_eur_rate(request)

        self.assertEqual(response.status_code, 200)

        response_data = json.loads(response.content)
        self.assertIn('average_usd_to_eur', response_data)
        self.assertAlmostEqual(response_data['average_usd_to_eur'], 1.2, places=2)

    def test_invalid_date_format(self):
        request = self.factory.get('/', {'start_date': '2023/01/01', 'end_date': '2023-01-05'})
        response = get_usd_to_eur_rate(request)

        self.assertEqual(response.status_code, 400)

        response_data = json.loads(response.content)
        self.assertIn('error', response_data)

    def test_end_date_before_start_date(self):
        request = self.factory.get('/', {'start_date': '2023-01-05', 'end_date': '2023-01-01'})
        response = get_usd_to_eur_rate(request)

        self.assertEqual(response.status_code, 400)

        response_data = json.loads(response.content)
        self.assertIn('error', response_data)
