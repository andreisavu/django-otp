from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib import auth

SECRET_PAGE = "/secret-page" # URL of secret page
ERROR_MESSAGE = "The username and password don't seem to match. Try again."

def home(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(SECRET_PAGE)
    else:
        return render_to_response('home.html')

def login(request):
    if request.method == 'GET':
        return HttpResponseRedirect('/')
    else:
        username = request.POST.get('username','')
        password = request.POST.get('password', '')

        user = auth.authenticate(username=username, password=password)

        if user is not None and user.is_active:
            auth.login(request, user)
            return HttpResponseRedirect(SECRET_PAGE)
        else:
            return render_to_response('home.html', {'error_message' : ERROR_MESSAGE})

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')

def secret_page(request):
    return render_to_response('secret-page.html')
