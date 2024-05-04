from datetime import datetime
from datetime import date

import logging
logger = logging.getLogger(__name__)

from django.forms import ModelForm
from event_manager.models import EventModel


class EventForm(ModelForm):
    def clean(self):
        self.cleaned_data = super().clean()
        # Check that the time is consistent.
        try:
            if self.cleaned_data['date'] < date.today():
                self.add_error('date', 'Invalid Input: Event cannot occur before current date.')
            
            if self.cleaned_data['start'] > self.cleaned_data['end']:
                self.add_error('start', 'Invalid Input: Event cannot start after the end time.')
                self.add_error('end', 'Invalid Input: Event cannot end before its start time.')
        except:
            pass
        
        return self.cleaned_data

    class Meta:
        model = EventModel
        fields = [ "title", "subtitle", "date", "location", "start", "end" ]
