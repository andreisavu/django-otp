import xmlrpclib as rpc

from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib import auth
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from captcha.fields import CaptchaField

from otp.models import UserService

RPC_SERVER_HOST = "http://192.168.1.5:8080/"
SECRET_PAGE = "/secret-page" # URL of secret page
ERROR_MESSAGE = "The username and password don't seem to match. Try again."

class MessageGateway:

    def __init__(self, url):
        self.url = url
        self.server = rpc.ServerProxy(url)

    def send(self, channel, msg, params):
        return self.server.send(channel, msg, params)

    def send_id(self, channel, params):
        return self.server.send_id(channel, params)

    def get_channels(self):
        return self.server.get_channels()

class MessageGatewayMock:

    def __init__(self, url):
        self.url = url

    def send(self, channel, msg, params):
        print "Send: %s, %s" % (channel, msg)
        return True

    def send_id(self, channel, params):
        print "SendID: %s" % channel
        return "12345"

    def get_channels(self):
        return [
            {
                'id':'smtp',
                'name':'Email',
                'description':'Use an email address for receiving the password',
                'params':{'to':'Adresa'}
            },
            {
                'id':'sms',
                'name':'SMS',
                'description':'Use a phone number to receive the password via SMS',
                'params':{'to':'Phone Number'}
            },
        ]

rpc_gateway = MessageGateway(RPC_SERVER_HOST)

ADAPTERS = []
SERVICES = []

for channel in rpc_gateway.get_channels():
    ADAPTERS.append((channel['id'], channel['description']))
    SERVICES.append(channel['id'])

class PassAdapterForm(forms.Form):
    adapter = forms.ChoiceField(choices=ADAPTERS, label="Send password by")
    captcha = CaptchaField()

class OneTimePassForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput(render_value=False))

class ModifyAccountForm(forms.Form):
    pass

def auth_user(username, password, request):
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

        return auth_user(username, password, request)

def onetime(request):
    post = request.method == 'POST'

    if not post or not request.POST.get('adapter', ''):
        return HttpResponseRedirect('/')

    form = PassAdapterForm(request.POST)

    if form.is_valid():
        username   = request.session['username']
        service_id = request.POST.get('adapter')

        user_param = UserService.objects.get(
            user = User.objects.get(username=username),
            service_id = service_id,
        )
        param = {'to': user_param.params}
        password = rpc_gateway.send_id(service_id, param)

        if not password:
            raise BackendError()

        request.session['password'] = password

        form = OneTimePassForm()
        return render_to_response('onetime-login.html', {'form' : form})

    return render_to_response('choose-adapter.html', {'form' : form})

def onetime_login(request):
    post   = request.method == 'POST'
    passwd = request.POST.get('password')
    if not post or not passwd:
        return HttpResponseRedirect('/')

    if passwd == request.session['password']:
        username = request.session['username']
        user = User.objects.get(username=username)
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        auth.login(request, user)
        return HttpResponseRedirect(SECRET_PAGE)

    return HttpResponseRedirect('/')

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

def modify_account(request):
    """
    """
    if request.method == 'POST' and request.POST['services']:
        for service_index, service_param in enumerate(request.POST.getlist('services')):
            if not service_param.strip():
                continue

            user_service = UserService(
                user = request.user,
                service_id = SERVICES[int(service_index)],
                params = service_param,
            )
            user_service.save()

        return HttpResponseRedirect('/modify_account')

    form = ModifyAccountForm()
    return render_to_response('modify-account.html', {
        'form' : form,
        'services' : ADAPTERS,
    })
