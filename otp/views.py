from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib import auth
from django import forms
from django.contrib.auth.forms import UserCreationForm

from captcha.fields import CaptchaField

SECRET_PAGE = "/secret-page" # URL of secret page
ERROR_MESSAGE = "The username and password don't seem to match. Try again."
ADAPTERS = (
    ('email', 'Email'),
    ('sms', 'SMS'),
    ('im', 'IM'),
)

class PassAdapterForm(forms.Form):
    adapter = forms.ChoiceField(choices=ADAPTERS, label="Send password by")
    captcha = CaptchaField()

class OneTimePassForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput(render_value=False))

def auth_user(username, password):
    user = auth.authenticate(username=username, password=password)

    if user is not None and user.is_active:
        auth.login(request, user)
        return HttpResponseRedirect(SECRET_PAGE)
    else:
        return render_to_response('home.html', {'error_message' : ERROR_MESSAGE})

def home(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(SECRET_PAGE)
    else:
        return render_to_response('home.html')

def login(request):
    if request.method == 'GET':
        return HttpResponseRedirect('/')
    else:
        username = request.POST.get('username', '')

        if request.POST.get('onetime', ''):
            request.session['username'] = username
            form = PassAdapterForm()
            return render_to_response('choose-adapter.html', {'form' : form})

        password = request.POST.get('password', '')

        return auth_user(username, password)

def onetime(request):
    post = request.method == 'POST'

    if not post or not request.POST.get('adapter', ''):
        return HttpResponseRedirect('/')

    form = PassAdapterForm(request.POST)

    if form.is_valid():
        form = OneTimePassForm()
        return render_to_response('onetime-login.html', {'form' : form})

    return render_to_response('choose-adapter.html', {'form' : form})

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')

def secret_page(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/')

    return render_to_response('secret-page.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect(SECRET_PAGE)
    else:
        form = UserCreationForm()
    return render_to_response("register.html", {
        'form': form,
    })
