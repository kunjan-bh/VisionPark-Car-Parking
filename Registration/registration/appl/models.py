from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from datetime import time
from datetime import timedelta, datetime

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    license_plate = models.CharField(max_length=50,default= '')
    location = models.CharField(max_length=100)
    selected_slot = models.CharField(max_length=50)
    start_time = models.DateTimeField()
    # end_time = models.TimeField(default=time(0, 0)) #shows midnight in administration
    end_time = models.DateTimeField() #shows midnight in administration
    booking_type = models.CharField(max_length=10)
    buffer_time = models.DurationField(default=timedelta(minutes=0))
    total_endtime = models.DateTimeField(default = datetime.combine(datetime.today(), time(0, 0, 0)))
    status = models.CharField(max_length=50, default = 'Pending..')
    payment = models.CharField(max_length=50, default = 'Pending..')

    def __str__(self):
        return f"{self.full_name} - {self.license_plate} - {self.location}"
