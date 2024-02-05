from django.db import models


# Create your models here.


class hubRegistration(models.Model):
    Hub_name = models.CharField(max_length=100)
    email = models.EmailField()
    mobile_number = models.CharField(max_length=20)
    telephone_number = models.CharField(max_length=20)
    address = models.CharField(max_length=200)
    operating_hours = models.CharField(max_length=100)
    hub_image = models.ImageField(upload_to='hubimages')
    hub_types = models.CharField(max_length=50, choices=[
        ('auto', 'Auto Repair'),
        ('towing', 'Towing'),
        ('bodyshop', 'Body Shop'),
        ('maintenance', 'Maintenance'),
        ('custom', 'Custom Work'),
        ('all', 'All'),
        ('others', 'Others'),
    ])
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)

    password = models.CharField(max_length=255)

    def __str__(self):
        return self.Hub_name


class Mechanic(models.Model):
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    hub = models.ForeignKey(hubRegistration, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
