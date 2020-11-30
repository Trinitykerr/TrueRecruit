from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from recruit.forms import RegistrationForm
from .models import User
# Create your views here.


def home(request):
    return render(request, 'recruit/home.html')


def registration_view(request):
    context = {}
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            # email = form.cleaned_data.get('email')
            # raw_password = form.cleaned_data.get('password1')
            # account = authenticate(email=email, password=raw_password)
            # login(request, account)
            return redirect('recruit:home')
        else:
            context['registration_form'] = form
    else:
        form = RegistrationForm
        context['registration_form'] = form

    return render(request, 'recruit/register.html', context)



