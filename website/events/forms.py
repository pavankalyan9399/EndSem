from django import forms
from django.forms import ModelForm
from .models import Venue, Event


# SUPERUSER EVENT FORM
class EventFormAdmin(ModelForm):
    class Meta:
        model=Event
        fields=("name", "event_date", "venue", "manager", "attendees", "description")
        labels={
            "name": "",
            "event_date": "",
            "venue": "Venue",
            "manager": "Manager",
            "attendees": "Attendees",
            "description": ""
        }
        widgets={
            "name": forms.TextInput(attrs={"class":'form-control', "placeholder": "Enter Your Event Name"}),
            "event_date": forms.TextInput(attrs={"class":'form-control', "placeholder": "Enter Event Date (YYYY-MM-DD HH:MM:SS)"}),
            "venue": forms.Select(attrs={"class":'form-select', "placeholder": "Enter Venue"}),
            "manager": forms.Select(attrs={"class":'form-select', "placeholder": "Enter Manager"}),
            "attendees": forms.SelectMultiple(attrs={"class":'form-control', "placeholder": "Enter Attendees"}),
            "description": forms.Textarea(attrs={"class":'form-control', "placeholder": "Enter Description"})
        }


# USER EVENT FORM
class EventForm(ModelForm):
    class Meta:
        model=Event
        fields=("name", "event_date", "venue", "attendees", "description")
        labels={
            "name": "",
            "event_date": "",
            "venue": "Venue",
            "attendees": "Attendees",
            "description": ""
        }
        widgets={
            "name": forms.TextInput(attrs={"class":'form-control', "placeholder": "Enter Your Event Name"}),
            "event_date": forms.TextInput(attrs={"class":'form-control', "placeholder": "Enter Event Date (YYYY-MM-DD HH:MM:SS)"}),
            "venue": forms.Select(attrs={"class":'form-select', "placeholder": "Enter Venue"}),
            "attendees": forms.SelectMultiple(attrs={"class":'form-control', "placeholder": "Enter Attendees"}),
            "description": forms.Textarea(attrs={"class":'form-control', "placeholder": "Enter Description"})
        }


class VenueForm(ModelForm):
    class Meta:
        model=Venue
        fields=("name", "address", "zipcode", "phone_number", "web", "email_address", "image")
        labels={
            "name": "",
            "address": "",
            "zipcode": "",
            "phone_number": "",
            "web": "",
            "email_address": "",
            "image": ""
        }
        widgets={
            "name": forms.TextInput(attrs={"class":'form-control', "placeholder": "Enter Your Venue Name"}),
            "address": forms.TextInput(attrs={"class":'form-control', "placeholder": "Enter Venue Address"}),
            "zipcode": forms.TextInput(attrs={"class":'form-control', "placeholder": "Enter Zipcode"}),
            "phone_number": forms.TextInput(attrs={"class":'form-control', "placeholder": "Enter Phone Number"}),
            "web": forms.TextInput(attrs={"class":'form-control', "placeholder": "Enter Venue Web Address"}),
            "email_address": forms.EmailInput(attrs={"class":'form-control', "placeholder": "Enter Email Address"})
        }