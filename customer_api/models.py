from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # customer information
    real_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    
    def __str__(self):
        return self.real_name