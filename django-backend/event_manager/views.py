from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from event_manager.forms import EventForm
from event_manager.models import EventModel

import logging
logger = logging.getLogger(__name__)

@login_required(login_url='/eventor/login')
def get_events(request: HttpRequest) -> HttpResponse:
    logger.debug(f"Getting all events for user {request.user}")
    all_events = EventModel.objects.all().filter(owner__id=request.user.id)
    events = []
    for event in all_events:
        events.append({"title": event.title, "id": event.id})
    return render(request, "my_events.html", {"my_events": events})

@login_required(login_url='/eventor/login')
def new_event(request: HttpRequest) -> HttpResponse:
    "Receives a request to create a new event."
    logger.debug(f"User {request.user} entering new event page.")
    newEvent = EventModel()
    template_state = {
            "id": id,
            "is_edit": True,
            "details": newEvent,
            "saved": False,
            "new_event_created": False,
            "form_errors": None,
        }

    if request.method == "POST":
        newEventForm = EventForm(request.POST, instance=newEvent)
        if newEventForm.is_valid():
            newEvent.owner = User.objects.get(id=request.user.id)
            logger.debug(f"User {request.user} created new event: {newEvent}.")
            newEventForm.save()
            template_state["event_date"] = newEventForm.cleaned_data["date"]
            template_state["event_date"] = newEvent.date.strftime('%Y-%m-%d'),
            template_state["event_start_time"] = newEvent.start.strftime('%H:%M'),
            template_state["event_end_time"] = newEvent.end.strftime('%H:%M'),
            template_state["new_event_created"] = True
            return get_events(request)
        else:
            template_state["form_errors"] = newEventForm.errors.as_data
            logger.debug(f"Event with id={id} has been submitted with errors: {newEventForm.errors.as_json()}")

    return render(request, "new_or_edit_event.html", template_state)

@login_required(login_url='/eventor/login')
def delete_event(request: HttpRequest, id: int) -> HttpResponse:
    "Receives a request to delete an existing event and return to the event page."
    logger.debug(f"User {request.user} attempting to delete event with id={id}.")
    try: 
        details = EventModel.objects.get(pk=id)
        logger.debug(f"Event {details} has been deleted.")
        details.delete()
    except EventModel.DoesNotExist:
        logger.debug(f"Event {details} does not exist.")
    return get_events(request)

@login_required(login_url='/eventor/login')
def edit_event(request: HttpRequest, id: int) -> HttpResponse:
    "Given an existing event, we want to edit it."
    logger.debug(f"User {request.user} attempting to edit event with id={id}.")
    try:
        details = EventModel.objects.get(pk=id)
    except EventModel.DoesNotExist:
        logger.debug(f"Event with id={id} does not exist.")
        return get_events(request)

    template_state = {
            "id": id,
            "is_edit": True,
            "details": details,
            "saved": False,
            "form_errors": None,
            "event_date": details.date.strftime('%Y-%m-%d'),
            "event_start_time": details.start.strftime('%H:%M'),
            "event_end_time": details.end.strftime('%H:%M'),
            }
    
    if request.method == "POST":
        modified_details = EventForm(request.POST, instance=details)
        logger.debug(f"User {request.user} submits event with id={id} for modification.")
        if modified_details.is_valid():
            modified_details.save()
            details = modified_details
            template_state["saved"] = True
            logger.debug(f"Event with id={id} modified.")
        else: 
            template_state["form_errors"] = modified_details.errors.as_data
            logger.debug(f"Event with id={id} has been submitted with errors: {modified_details.errors.as_json()}")
    
    return render(request, "new_or_edit_event.html", template_state)

@login_required(login_url='/eventor/login')
def event_details(request: HttpRequest, id: int) -> HttpResponse:
    "Given an event id, fetch it from the database and present it."
    logger.debug(f"User {request.user} attempting to accessing event with id={id}.")
    try:
        details = EventModel.objects.get(pk=id)
        logger.debug(f"Event with id={id} accessed.")
    except EventModel.DoesNotExist:
        logger.debug(f"Event with id={id} does not exist.")
        return get_events(request)

    template_state = {
            "id": id,
            "details": details
    }

    return render(request, "event_details.html", template_state)
