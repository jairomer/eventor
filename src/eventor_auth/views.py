import logging
logger = logging.getLogger(__name__)

from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required

from .forms import LoginUserForm, RegistrationForm 

# Create your views here.
def loginUser(request: HttpRequest) -> HttpResponse:
    template_state = {
        "not_found": False,
        "error": False,
    }
    if request.user.is_authenticated:
        logger.debug(f"User has already been authenticated. Redirecting to main page.")
        return redirect("/eventor/events/")

    if (request.method == 'POST'):
        # TODO: Add bruteforce protection.
        loginForm = LoginUserForm(request.POST)
        if loginForm.is_valid():
            logger.debug(f"{loginForm} is valid, checking with database")
            try:
                user = authenticate(
                        username=loginForm.cleaned_data['username'],
                        password=loginForm.cleaned_data['password'])
                if user is not None:
                    logger.debug(f"{loginForm} was successful, redirecting to main page.")
                    login(request, user)
                    return redirect("/eventor/events/")
            except Exception as e:
                logger.debug(f"Got exception '{e}'")
                template_state['error'] = True
                return render(request, "login.html", template_state)
            else:
                # TODO: log an attempt in the bruteforce protection.
                template_state["not_found"] = True
                logger.debug(f"{loginForm} was unsuccessful. User not found.")
        else:
            logger.debug("Login form is not valid.") 
            logger.debug(loginForm.errors.as_text)

    return render(request, "login.html", template_state)

def signin(request: HttpRequest) -> HttpResponse:
    template_state = {
            "form_errors": None,
            "user": None,
            "email": None,
            "existing": False,
    }
    if request.method == "POST":
        # TODO: Log new registration in antispamming system.
        registrationForm = RegistrationForm(request.POST)
        if registrationForm.is_valid():
            username = registrationForm.fields['username']
            email = registrationForm.fields['email']
            if username:
                template_state['user'] = username
            if email:
                template_state['email'] = email

            try:
                user = User.objects.get(username__exact=username, email__exact=email)
            except ObjectDoesNotExist:
                template_state['existing'] = False
            except Exception as e:
                logger.debug(f"Querying for user returned: {e}")
                return HttpResponse("Service Unavailable", status=503)

            if not template_state['existing']:
                logger.debug(f"User is not registered in the system. Registering.")
                user = User(
                        username=registrationForm.cleaned_data['username'],
                        email=registrationForm.cleaned_data['email'],
                        first_name=registrationForm.cleaned_data['username'])
                user.set_password(registrationForm.cleaned_data['password'])
                user.save()
                logger.debug(f"{registrationForm} was successfuly registered.")
                return redirect("/eventor/login/")
            else:
                logger.debug(f"There is already a user with username '{username}' with email '{email}'")
                registrationForm.add_error("username", 'There is already a user with that username/email combination.')
                template_state['existing'] = True
        else:
            logger.debug(f"Received an invalid registration form")
        template_state["form_errors"] = registrationForm.errors.as_data

    return render(request, "signin.html", template_state)

def account_recovery(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        # An existing email should be in the form. 
        # Check against bruteforce protection that this same email has not been submitted in the last 5 minutes. 
        #   IF < 5 minutes: Ask to try again later.
        #   Otherwise
        # Send an email with a link and a code to a page that allows the user to change its credentials. 
        # Send a notification to the user that his credentials have changed.
        # Ask her to login with new credentials..
        return render(request, "login.html", {})
    return render(request, "account_recovery.html", {})

def password_reset(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        # The same valid password should be in both fields. 
        # If password has not changed in the past minute, then the password field for this user should be updated.
        # Otherwise ask them to try again later.
        return render(request, "login.html", {})
    return render(request, "password_reset.html", {})

@login_required(login_url='/eventor/login')
def logoutUser(request: HttpRequest) -> HttpResponse:
    logout(request)
    return redirect("/eventor/login")
