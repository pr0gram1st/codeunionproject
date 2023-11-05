
from django.core.management import call_command
from .models import Currency
from io import StringIO
import unittest
from unittest.mock import patch


class CommandsTestCase(unittest.TestCase):
    def test_set_currency_rate(self):
        currency = Currency.objects.create(name="USD", rate=380)
        out = StringIO()
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            call_command('manage_currency', 'update', '--id', currency.id, '--rate', 400, stdout=out)
        currency.refresh_from_db()
        self.assertEqual(currency.rate, 400)
        self.assertIn("Currency USD updated to 400.0 KZT", out.getvalue())

    def test_set_currency_rate_invalid_currency_id(self):
        out = StringIO()
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            call_command('manage_currency', 'update', '--id', 999, '--rate', 400, stdout=out)
        self.assertIn("Currency not found", out.getvalue())

    def test_get_currency_rate_invalid_currency_id(self):
        out = StringIO()
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            call_command('manage_currency', 'get', '--id', 999, stdout=out)
        self.assertIn("Currency not found", out.getvalue())
    
    @patch('currency_rates.management.commands.update_currency_rates.requests.get')
    def test_update_currency_rates(self, mock_get):
        response_text = """
        <?xml version="1.0" encoding="UTF-8"?>
        <rss version="2.0">
            <channel>
                <item>
                    <title>USD</title>
                    <description>380.50</description>
                </item>
                <item>
                    <title>EUR</title>
                    <description>450.75</description>
                </item>
            </channel>
        </rss>
        """
        mock_get.return_value.status_code = 200
        mock_get.return_value.text = response_text

        out = StringIO()
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            call_command('update_currency_rates', stdout=out)

        self.assertIn("Currency rates updated successfully", out.getvalue())

    @patch('currency_rates.management.commands.update_currency_rates.requests.get')
    def test_update_currency_rates_error(self, mock_get):
        mock_get.return_value.status_code = 404

        out = StringIO()
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            call_command('update_currency_rates', stdout=out)

        self.assertIn("Failed to fetch data from the source", out.getvalue())


