from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import GlucoseLevel
from django.utils import timezone
import datetime

class GlucoseLevelTests(APITestCase):

    def setUp(self):
        self.user_id = "test"
        self.glucose_value = 150.0
        self.timestamp = timezone.now()
        self.device_name = "Apple Watch"
        self.device_serial_number = "S34DFT678"
        self.level = GlucoseLevel.objects.create(user_id=self.user_id, timestamp=self.timestamp,
                                                 glucose_value=self.glucose_value,
                                                 device_name=self.device_name,
                                                 device_serial_number=self.device_serial_number)

    def test_get_glucose_levels(self):
        url = reverse('glucoselevel-list')
        response = self.client.get(url, {'user_id': self.user_id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['user_id'], self.user_id)
        self.assertEqual(response.data['results'][0]['glucose_value'], self.glucose_value)


    def test_get_glucose_level_detail(self):
        url = reverse('glucoselevel-detail', args=[self.level.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user_id'], self.user_id)
        self.assertEqual(response.data['glucose_value'], self.glucose_value)

    def test_post_glucose_level(self):
        url = reverse('glucoselevel-create')
        data = {
            'user_id': self.user_id,
            'timestamp': self.timestamp.isoformat(),
            'glucose_value': 160.0,
            "device_name": self.device_name,
            "device_serial_number": self.device_serial_number,
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['user_id'], self.user_id)
        self.assertEqual(response.data['glucose_value'], 160.0)

    def test_pagination_and_ordering(self):
        # Create additional records
        GlucoseLevel.objects.create(user_id=self.user_id, timestamp=self.timestamp - datetime.timedelta(days=1), glucose_value=140.0)
        GlucoseLevel.objects.create(user_id=self.user_id, timestamp=self.timestamp + datetime.timedelta(days=1), glucose_value=170.0)

        url = reverse('glucoselevel-list')
        response = self.client.get(url + f"?user_id={self.user_id}&ordering=glucose_value&page_size=2")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

        self.assertEqual(response.data['results'][0]['glucose_value'], 140.0)

        response = self.client.get(url, {'user_id': self.user_id, 'ordering': '-glucose_value', 'page_size': 2})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
        self.assertEqual(response.data['results'][0]['glucose_value'], 170.0)
