from django.test import TestCase, RequestFactory
from django.contrib.auth.models import AnonymousUser, User
from .views import *

class EventCrudTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
                username="testUser", email="test@email.com", password="secret_test"
                )
        #self.event = EventModel(
        #    title="test_title",
        #    subtitle="test_subtitle",
        #    date=datetime(2024, 4, 10, 15, 30),
        #    start=datetime.time(12, 0),
        #    end=datetime.time(13, 0),
        #    nearestStation="Tetuan",
        #    location="Test Location")
        #self.event.save()

    def test_events_can_be_accessed(self):
        request = self.factory.get("eventor/events/")
        # TODO: Test with authentication.
        request.user = self.user
        #request.user = AnonymousUser()
        response = get_events(request)
        self.assertEqual(response.status_code, 200)
