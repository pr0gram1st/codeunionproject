import requests
from django.core.management.base import BaseCommand
from currency_rates.models import Currency

class Command(BaseCommand):
    help = 'Set new currency rate or get the current'

    def add_arguments(self, parser):
        parser.add_argument('action', choices=['update', 'get'])
        parser.add_argument('--id', type=int)
        parser.add_argument('--rate', type=float)

    def get_currency_rate(self, currency_id):
        try:
            obj = Currency.objects.get(id=currency_id)
            self.stdout.write(f'Currency ID: {obj.id}')
            self.stdout.write(f'Currency Name: {obj.name}')
            self.stdout.write(f'Currency Rate: {obj.rate} KZT')
        except Currency.DoesNotExist:
            self.stdout.write(self.style.ERROR('Currency not found'))

    def set_currency_rate(self, currency_id, new_rate):
        try:
            obj = Currency.objects.get(id=currency_id)
            obj.rate = new_rate
            obj.save()
            self.stdout.write(self.style.SUCCESS(f'Currency {obj.name} updated to {new_rate} KZT'))
        except Currency.DoesNotExist:
            self.stdout.write(self.style.ERROR('Currency not found'))

    def handle(self, *args, **options):
        action = options['action']
        currency_id = options['id']
        new_rate = options['rate']

        if action == 'update':
            if currency_id is None or new_rate is None:
                self.stdout.write(self.style.ERROR('Both currency ID and rate are required for update'))
            else:
                self.set_currency_rate(currency_id, new_rate)
        elif action == 'get':
            if currency_id is None:
                self.stdout.write(self.style.ERROR('Currency ID is required for viewing'))
            else:
                self.get_currency_rate(currency_id)
