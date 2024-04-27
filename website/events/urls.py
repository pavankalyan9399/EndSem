from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("admin/", views.home, name="admin"),
    path("<int:year>/<str:month>/", views.home, name="home"),
    path("events", views.all_events, name="list-event"),
    path("venue", views.all_venues, name="list-venue"),
    path("search_events", views.search_events, name="search-events"),
    path("search_venues", views.search_venues, name="search-venues"),
    path("add_venue", views.add_venue, name="add-venue"),
    path("add_event", views.add_event, name="add-event"),
    path("show_venue/<venue_id>", views.show_venue, name="show-venue"),
    path("show_event/<event_id>", views.show_event, name="show-event"),
    path("update_venue/<venue_id>", views.update_venue, name="update-venue"),
    path("update_event/<event_id>", views.update_event, name="update-event"),
    path("delete_event/<event_id>", views.delete_event, name="delete-event"),
    path("delete_venue/<venue_id>", views.delete_venue, name="delete-venue"),
    path("text_venue", views.text_venue, name="text-venue"),
    path("text_event", views.text_event, name="text-event"),
    path("csv_venue", views.csv_venue, name="csv-venue"),
    path("csv_event", views.csv_event, name="csv-event"),
    path("pdf_venue", views.pdf_venue, name="pdf-venue"),
    path("pdf_event", views.pdf_event, name="pdf-event"),
    path("my_events", views.my_events, name="my-events"),
]


############     PATH CONVERTORS     ##############
# <int:year> is path converters
# There are several path convertors
# int: for numbers
# str: for strings
# path: for whole urls and slash /
# slug: hyphens '-' and underscores '_'
# UUID: universal unique identifier