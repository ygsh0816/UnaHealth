import os
import csv
from datetime import datetime
from django.core.management.base import BaseCommand
from ...models import GlucoseLevel


class Command(BaseCommand):
    help = 'Load glucose levels from CSV files'

    def handle(self, *args, **kwargs):
        data_dir = 'app/sample_data_files'
        for filename in os.listdir(data_dir):
            if filename.endswith('.csv'):
                user_id = filename.split('.')[0]
                with open(os.path.join(data_dir, filename), 'r') as csvfile:
                    reader = csv.DictReader(csvfile)
                    for row in reader:
                        original_datetime_str = row['Gerätezeitstempel']
                        datetime_obj = datetime.strptime(original_datetime_str, "%d-%m-%Y %H:%M")
                        formatted_datetime_str = datetime_obj.strftime("%Y-%m-%d %H:%M")

                        try:
                            glucose_value = int(row['Glukosewert-Verlauf mg/dL'])
                        except ValueError:
                            glucose_value = None

                        GlucoseLevel.objects.create(
                            user_id=user_id,
                            device_name=row['Gerät'],
                            device_serial_number=row['Seriennummer'],
                            timestamp=formatted_datetime_str,
                            glucose_value=glucose_value
                        )
        self.stdout.write(self.style.SUCCESS('Data loaded successfully'))
