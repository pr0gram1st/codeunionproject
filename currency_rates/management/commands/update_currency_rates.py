import schedule
import time
import requests
import xml.etree.ElementTree as ET
from decimal import Decimal
from django.core.management.base import BaseCommand
from currency_rates.models import Currency

class Command(BaseCommand):
    help = 'Update currency rates from RSS feed'

    def update_currency_rates(self):
        try:
            response = requests.get('http://www.nationalbank.kz/rss/rates_all.xml')
            if response.status_code == 200:
                tree = ET.fromstring(response.text)
                for currency_element in tree.findall('.//channel/item'):
                    self.stdout.write("I was here")
                    name = currency_element.find('title').text
                    rate = currency_element.find('description').text
                    rate = Decimal(rate)
                    Currency.objects.update_or_create(name=name, defaults={'rate': rate})
                self.stdout.write(self.style.SUCCESS('Currency rates updated successfully'))
            else:
                self.stdout.write(self.style.ERROR('Failed to fetch data from the source'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error: {str(e)}'))

    def handle(self, *args, **options):
        schedule.every().hour.at(':00').do(self.update_currency_rates)
        
        while True:
            schedule.run_pending()
            time.sleep(1)
