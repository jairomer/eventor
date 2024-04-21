"""
URL configuration for eventor project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from event_manager.views import get_events, new_event, event_details, edit_event, delete_event
from eventor_auth.views import loginUser, logoutUser, signin, account_recovery, password_reset

urlpatterns = [
    path("admin/", admin.site.urls),
    path("eventor/events/", get_events),
    path("eventor/new_event/", new_event),
    path("eventor/event/<int:id>/", event_details),
    path("eventor/event/edit/<int:id>/", edit_event),
    path("eventor/event/delete/<int:id>/", delete_event),
    path("eventor/login/", loginUser),
    path("eventor/logout/", logoutUser),
    path("eventor/signin/", signin),
    path("eventor/recovery/", account_recovery),
    path("eventor/recovery/<int:id>/", password_reset),
    path("", get_events),
]
