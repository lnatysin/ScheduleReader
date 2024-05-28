from django.db import models

# Create your models here.
# schedule_app/models.py

from django.db import models

class Employee(models.Model):
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    position = models.CharField(max_length=50)
    # Add any other fields specific to employees (e.g., address, hire date, etc.)

    class Meta:
        app_label = 'schedule_app'

    def __str__(self):
        return self.name
