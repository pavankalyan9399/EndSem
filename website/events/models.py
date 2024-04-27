from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

def get_superuser():
    # Retrieve the superuser from the User model
    superuser = User.objects.filter(is_superuser=True).first()
    if superuser:
        return superuser.id
    return None

class Venue(models.Model):
    name = models.CharField("Venue Name", max_length=200)
    address = models.CharField(max_length=300)
    zipcode = models.CharField("Zipcode", max_length=15)
    phone_number = models.CharField("Phone Number", max_length=15, blank=True)
    web = models.URLField("Website Address", blank=True)
    email_address = models.EmailField("Email Address", blank=True)
    owner = models.IntegerField("Venue Owner", blank=False)
    image = models.ImageField(null=True, blank=True, upload_to="images/")

    def __str__(self):
        return self.name


class Event(models.Model):
    name = models.CharField("Event Name", max_length=200)
    event_date = models.DateTimeField("Event Date")
    venue = models.ForeignKey(Venue, blank=True, null=True, on_delete=models.CASCADE)
    manager = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default=get_superuser, related_name="manager")
    description = models.TextField(blank=True)
    attendees = models.ManyToManyField(User, blank=True, related_name="attendees")

    def __str__(self):
        return self.name