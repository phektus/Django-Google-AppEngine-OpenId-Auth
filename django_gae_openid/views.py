from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template.context import RequestContext

from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.conf import settings

from django_gae_openid import forms

from google.appengine import api as gae_api


def login_begin(request):
    """basic login"""
    domain = check_google_user(request)
    if domain is not None:
        return redirect('/')
            
    
    if request.method == 'POST':
        form = forms.OpenIDLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            domain = email.split('@').pop()
            return redirect(gae_api.users.create_login_url(dest_url=settings.OPENID_LOGIN_DESTINATION,
                _auth_domain=None,
                federated_identity=domain))
    else:
        form = forms.OpenIDLoginForm()

    return render_to_response('openid/login.html', {
        'form': form,
    })  


# @csrf_exempt
def login_complete(request):
    return redirect('/accounts/login/')

def check_google_user(request):
    """validates current google login"""
    google_user = gae_api.users.get_current_user()
    if google_user:
        username = google_user.email()
        domain = google_user.email().split('@').pop()
        user = authenticate(username=username,domain=domain)
        if user is not None:
             login(request, user)             
             return domain
    return None

def logout_view(request):
    logout(request)    
    return redirect(gae_api.users.create_logout_url(dest_url=settings.OPENID_LOGOUT_DESTINATION,
        _auth_domain=None))
