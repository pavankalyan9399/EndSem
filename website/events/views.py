from django.shortcuts import render, redirect
import calendar
from calendar import HTMLCalendar
from datetime import datetime

# Importing Models
from .models import Event, Venue
from django.contrib.auth.models import User

from .forms import VenueForm, EventForm, EventFormAdmin
from django.http import HttpResponseRedirect
from django.http import HttpResponse
import csv
from django.contrib import messages

# Importing libraries for pdf generator
from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter

# Importing for Pagination
from django.core.paginator import Paginator


# Create your views here.
def home(request, year=datetime.now().year, month=datetime.now().strftime("%B")):
    month=month.capitalize()
    # changing month into integer like january to 1
    month_number = list(calendar.month_name).index(month)
    cal = HTMLCalendar().formatmonth(year, month_number)
    now = datetime.now()
    current_year = now.year
    time = now.strftime("%I:%M:%S %p")
    events = Event.objects.filter(event_date__year=year, event_date__month=month_number).order_by("-event_date", "name")
    return render(request, "events/home.html",{"events": events,"year":year, "month":month, "cal":cal,
                                            "current_year":current_year, "time": time, "datetime": now})


def search_events(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            searched = request.POST["searched"]
            if not searched:
                messages.success(request, ("You didn't search anything!!!"))
                return redirect("home")
            events = Event.objects.filter(name__icontains=searched).order_by("-event_date", "name")
            messages.success(request, (f"Results of search \"{searched}\""))
            return render(request, "events/search_events.html", {"searched": searched, "events": events, "datetime": datetime.now()})
        else:
            messages.success(request, ("You need to search first!!!"))
            return redirect("home")
    else:
        messages.success(request, ("You aren't Authorized to Search Events. Please Login/Register First !!!"))
        return redirect("login")


def search_venues(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            searched = request.POST["searched"]
            if not searched:
                messages.success(request, ("You didn't search anything!!!"))
                return redirect("search-venues")
            venues = Venue.objects.filter(name__icontains=searched).order_by("name")
            messages.success(request, (f"Results of search \"{searched}\""))
            return render(request, "events/search_venues.html", {"searched": searched, "venues": venues, "datetime": datetime.now()})
        else:
            return render(request, "events/search_venues.html", {})
    else:
        messages.success(request, ("You aren't Authorized to Search Venues. Please Login/Register First !!!"))
        return redirect("login")


def all_events(request):
    # events_list = Event.objects.all().order_by("event_date", "name")
    p = Paginator(Event.objects.all().order_by("-event_date", "name"), 6)
    page = request.GET.get("page")
    events = p.get_page(page)
    # return render(request, "events/list_event.html", {"events_list":events_list})
    return render(request, "events/list_event.html", {"events": events, "datetime": datetime.now()})


def all_venues(request):
    # venues_list = Venue.objects.all().order_by("name")
    # Setting up pagination
    p = Paginator(Venue.objects.all().order_by("name"), 6)
    page = request.GET.get("page")
    venues = p.get_page(page)
    for venue in venues:
        print("User Id :", request.user.id, "\tVenue Onwer :", venue.owner)
    # return render(request, "events/list_venue.html", {"venues_list": venues_list})
    return render(request, "events/list_venue.html", {"venues": venues})


def show_event(request, event_id):
    if request.user.is_authenticated:
        event = Event.objects.get(pk=event_id)
        return render(request, "events/show_event.html", {"event": event, "datetime": datetime.now()})
    else:
        messages.success(request, ("You aren't Authorized to See Event's Details. Please Login/Register First !!!"))
        return redirect("list-event")


def show_venue(request, venue_id):
    if request.user.is_authenticated:
        venue = Venue.objects.get(pk=venue_id)
        venue_owner = User.objects.get(pk=venue.owner)
        events = Event.objects.filter(venue=venue.id).order_by("-event_date", "name")
        return render(request, "events/show_venue.html", {"venue": venue, "events": events, "venue_owner": venue_owner})
    else:
        messages.success(request, ("You aren't Authorized to See Venue's Details. Please Login/Register First !!!"))
        return redirect("list-venue")


def update_event(request, event_id):
    if request.user.is_authenticated:
        event = Event.objects.get(pk=event_id)
        if request.user==event.manager:
            if event.event_date.date()>=datetime.now().date():
                if event.event_date.time()>datetime.now().time():
                    name=event.name
                    if request.user.is_superuser:
                        form = EventFormAdmin(request.POST or None, instance=event)
                    else:
                        form = EventForm(request.POST or None, instance=event)
                    if form.is_valid():
                        form.save()
                        messages.success(request, (f"Details of Event \"{name}\" is Updated !!!"))
                        return redirect("list-event")
                    return render(request, "events/update_event.html", {"event": event, "form": form})
            else:
                messages.success(request, (f"Cannot Update Finished Event !!!"))
        else:
            messages.success(request, (f"Event can only be Updated by Manager !!!"))
        return redirect("list-event")
    else:
        messages.success(request, ("You aren't Authorized to Update Event. Please Login/Register First !!!"))
        return redirect("login")


def update_venue(request, venue_id):
    if request.user.is_authenticated:
        venue = Venue.objects.get(pk=venue_id)
        name=venue.name
        form = VenueForm(request.POST or None, request.FILES or None, instance=venue)
        if form.is_valid():
            messages.success(request, (f"Details of Venue \"{name}\" is Updated !!!"))
            form.save()
            return redirect("list-venue")
        return render(request, "events/update_venue.html", {"venue": venue, "form": form})
    else:
        messages.success(request, ("You aren't Authorized to Update Venue. Please Login/Register First !!!"))
        return redirect("login")


def add_event(request):
    if request.user.is_authenticated:
        submitted=False
        if request.method=="POST":
            if request.user.is_superuser:
                form=EventFormAdmin(request.POST)
                if form.is_valid():
                    name=form.cleaned_data["name"]
                    form.save()
                    messages.success(request, (f"Event \"{name}\" Added !!!"))
            else:
                form=EventForm(request.POST)
                if form.is_valid():
                    name=form.cleaned_data["name"]
                    event=form.save(commit=False)
                    event.manager=request.user
                    event.save()
                    messages.success(request, (f"Event \"{name}\" Added !!!"))
            return HttpResponseRedirect("add_event?submitted=True")
        else:
            if request.user.is_superuser:
                form=EventFormAdmin
            else:
                form=EventForm
            if "submitted" in request.GET:
                submitted=True
                return redirect("list-event")
        return render(request, "events/add_event.html", {"form":form, "submitted":submitted})
    else:
        messages.success(request, ("You aren't Authorized to Add Events. Please Login/Register First !!!"))
        return redirect("login")


def add_venue(request):
    if request.user.is_authenticated:
        submitted=False
        if request.method=="POST":
            form=VenueForm(request.POST, request.FILES)
            if form.is_valid():
                name=form.cleaned_data["name"]
                venue=form.save(commit=False)
                venue.owner=request.user.id
                venue.save()
                messages.success(request, (f"Venue \"{name}\" Added !!!"))
                return HttpResponseRedirect("add_venue?submitted=True")
        else:
            form=VenueForm
            if "submitted" in request.GET:
                submitted=True
                return redirect("list-venue")
        return render(request, "events/add_venue.html", {"form":form, "submitted":submitted})
    else:
        messages.success(request, ("You aren't Authorized to Add Venues. Please Login/Register First !!!"))
        return redirect("login")


def delete_event(request, event_id):
    if request.user.is_authenticated:
        event = Event.objects.get(pk=event_id)
        if request.user==event.manager:
            if event.event_date.date()>datetime.now().date():
                name=event.name
                event.delete()
                messages.success(request, (f"Event \"{name}\" Deleted !!!"))
            else:
                messages.success(request, (f"Cannot Delete Finished Event !!!"))
        else:
            messages.success(request, (f"Event can only be Deleted by Manager !!!"))
        return redirect("list-event")
    else:
        messages.success(request, ("You aren't Authorized to Delete the Event. Please Login/Register First !!!"))
        return redirect("login")


def delete_venue(request, venue_id):
    if request.user.is_authenticated:
        venue = Venue.objects.get(pk=venue_id)
        name=venue.name
        venue.delete()
        messages.success(request, (f"Venue \"{name}\" Deleted !!!"))
        return redirect("list-venue")
    else:
        messages.success(request, ("You aren't Authorized to Delete the Venue. Please Login/Register First !!!"))
        return redirect("login")


def my_events(request):
    if request.user.is_authenticated:
        p = Paginator(Event.objects.filter(attendees=request.user.id).order_by("-event_date", "name"), 6)
        page = request.GET.get("page")
        events = p.get_page(page)
        # return render(request, "events/list_event.html", {"events_list":events_list})
        return render(request, "events/my_events.html", {"events": events, "datetime": datetime.now()})
    else:
        messages.success(request, ("You aren't Logged in. Please Login/Register First to view your Events !!!"))
        return redirect("login")



def text_event(request):
    if request.user.is_authenticated:
        response = HttpResponse(content_type="text/plain")
        response["Content-Disposition"]="attachment; filename=events.txt"
        lines=[]
        events = Event.objects.all().order_by("event_date","name")
        for event in events:
            lines.append(f"event Name: {event.name}\nEvent Date: {event.event_date}\nVenue: {event.venue}\nManager: {event.manager}\nDescription: {event.description}\n\n\n")
        response.writelines(lines)
        return response
    else:
        messages.success(request, ("You must be Logged in to Download Files. Please Login/Register First !!!"))
        return redirect("login")




######### Downloads ###############

# Generate text file of venue list
def text_venue(request):
    if request.user.is_authenticated:
        response = HttpResponse(content_type="text/plain")
        response["Content-Disposition"]="attachment; filename=venues.txt"
        lines=[]
        venues = Venue.objects.all().order_by("name")
        for venue in venues:
            lines.append(f"Venue Name: {venue.name}\nAddress: {venue.address}\nZipcode: {venue.zipcode}\nPhone Number: {venue.phone_number}\nWebsite: {venue.web}\nEmail Address: {venue.email_address}\n\n\n")
        response.writelines(lines)
        return response
    else:
        messages.success(request, ("You must be Logged in to Download Files. Please Login/Register First !!!"))
        return redirect("login")


def csv_event(request):
    if request.user.is_authenticated:
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"]="attachment; filename=events.csv"
        events = Event.objects.all().order_by("name")
        # Create a csv writer
        writer = csv.writer(response)
        # Adding columns heading
        writer.writerow(["Name", "Date", "Venue", "Manager", "Description"])
        for event in events:
            writer.writerow([event.name, event.event_date, event.venue, event.manager, event.description])
        return response
    else:
        messages.success(request, ("You must be Logged in to Download Files. Please Login/Register First !!!"))
        return redirect("login")


def csv_venue(request):
    if request.user.is_authenticated:
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"]="attachment; filename=venues.csv"
        venues = Venue.objects.all().order_by("name")
        # Create a csv writer
        writer = csv.writer(response)
        # Adding columns heading
        writer.writerow(["Venue Name", "Address", "Zipcode", "Phone Number", "Website", "Email Address"])
        for venue in venues:
            writer.writerow([venue.name, venue.address, venue.zipcode, venue.phone_number, venue.web, venue.email_address])
        return response
    else:
        messages.success(request, ("You must be Logged in to Download Files. Please Login/Register First !!!"))
        return redirect("login")


def pdf_event(request):
    if request.user.is_authenticated:
        # Create bytestream buffer
        buf = io.BytesIO()
        c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
        textobj = c.beginText()
        textobj.setTextOrigin(inch, inch)
        events = Event.objects.all()
        lines=[]
        for event in events:
            lines.append(f"Event Name: {event.name}")
            lines.append(f"Event Date: {event.event_date}")
            lines.append(f"Venue: {event.venue}")
            lines.append(f"Manager: {event.manager}")
            lines.append(f"Description: {event.description}")
            lines.append(" ")
            lines.append(" ")
        for line in lines:
            textobj.textLine(line)
        c.drawText(textobj)
        c.showPage()
        c.save()
        buf.seek(0)
        return FileResponse(buf, as_attachment=True, filename="events.pdf")
    else:
        messages.success(request, ("You must be Logged in to Download Files. Please Login/Register First !!!"))
        return redirect("login")


# PIP INSTALL reportlab
def pdf_venue(request):
    if request.user.is_authenticated:
        # Create bytestream buffer
        buf = io.BytesIO()
        c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
        textobj = c.beginText()
        textobj.setTextOrigin(inch, inch)
        venues = Venue.objects.all()
        lines=[]
        for venue in venues:
            lines.append(f"Venue Name: {venue.name}")
            lines.append(f"Address: {venue.address}")
            lines.append(f"Zipcode: {venue.zipcode}")
            lines.append(f"Phone Number: {venue.phone_number}")
            lines.append(f"Website: {venue.web}")
            lines.append(f"Email Address: {venue.email_address}")
            lines.append(" ")
            lines.append(" ")
        for line in lines:
            textobj.textLine(line)
        c.drawText(textobj)
        c.showPage()
        c.save()
        buf.seek(0)
        return FileResponse(buf, as_attachment=True, filename="venues.pdf")
    else:
        messages.success(request, ("You must be Logged in to Download Files. Please Login/Register First !!!"))
        return redirect("login")



