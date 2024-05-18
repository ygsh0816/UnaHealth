from django.db import models


class GlucoseLevel(models.Model):
    device_name = models.CharField(max_length=100)
    device_serial_number = models.CharField(max_length=100)
    user_id = models.CharField(max_length=100)
    timestamp = models.DateTimeField()
    glucose_value = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f'User {self.user_id} - {self.glucose_value} at {self.timestamp}'
