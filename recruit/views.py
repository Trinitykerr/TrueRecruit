from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from recruit.forms import RegistrationForm, ContactForm, CreatePlayer, CreateCoach, LoginForm
from django.core.paginator import Paginator
from .models import Player, PlayerMore, CoachMore
from .models import Coach
from django.template import loader
from django.contrib import messages
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
import pdfkit
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic.edit import FormView
# from.forms import ContactForm
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
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            account = authenticate(email=email, password=raw_password)
            type1 = form.cleaned_data.get("type")
            login(request, account)

            if type1 == 'PLAYER':
                return redirect('recruit:createplayer')
            else:
                return redirect('recruit:createcoach')
        else:
            context['registration_form'] = form
    else:
        form = RegistrationForm
        context['registration_form'] = form

    return render(request, 'recruit/register.html', context)


def player_list(request):
    player_object = PlayerMore.objects.all()
    player_state = request.GET.get('player_state')

    if player_state != '' and player_state is not None:
        player_object = player_object.filter(state__icontains= player_state)

    paginator = Paginator(player_object, 5)
    page = request.GET.get('page')
    player_object = paginator.get_page(page)
    return render(request, 'recruit/playerlist.html', {'player_object':player_object})


def coach_list(request):
    coach_object = CoachMore.objects.all()
    coach_state = request.GET.get('coach_state')

    if coach_state != '' and coach_state is not None:
        coach_object = coach_object.filter(state__icontains= coach_state)

    paginator = Paginator(coach_object, 5)
    page = request.GET.get('page')
    coach_object = paginator.get_page(page)
    return render(request, 'recruit/coachlist.html', {'coach_object':coach_object})


class PlayerDetail(DetailView):
    model = PlayerMore
    template_name = 'recruit/playerdetail.html'


def CoachDetail(request, id):
    coach = CoachMore.objects.get(pk=id)

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Your message has been sent')
            return redirect('recruit:coach_list')
    else:
        form = ContactForm()
    context = {
        'coach':coach,
        'form':form
    }
    return render(request, 'recruit/coachdetail.html', context)


def PlayerPrint(request, id):
    player = PlayerMore.objects.get(pk=id)
    template = loader.get_template('recruit/print.html')
    html = template.render({'player': player})
    filename = 'RecruitPlayer.pdf'
    html.options = {
        'title': 'RecruitPlayer',
        'page-size': 'Letter',
        'encoding': 'UTF-8',
    }
    config = pdfkit.configuration(wkhtmltopdf='C:\\wkhtmltopdf\\bin\\wkhtmltopdf.exe')
    pdf = pdfkit.from_string(html, False, configuration=config)
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment'

    return response


@login_required
def createplayer(request):

    if request.method == 'POST':
        form = CreatePlayer(request.POST)
        if form.is_valid():
            form.save()
            name = form.cleaned_data.get('name')
            messages.success(request, f'Welcome {name}! Your profile is created')
            return redirect('recruit:coach_list')

    else:

        form = CreatePlayer()
        return render(request, 'recruit/createplayer.html', {'form':form})


@login_required
def createcoach(request):

    if request.method == 'POST':
        form = CreateCoach(request.POST)
        if form.is_valid():
            form.save()
            name = form.cleaned_data.get('name')
            messages.success(request, f'Welcome {name}! Your profile is created')
            return redirect('recruit:player_list')

    else:

        form = CreateCoach()
        return render(request, 'recruit/createcoach.html', {'form':form})



@login_required
def profilepage(request):
    return render(request, 'recruit/profile.html')



def Logout(request):
    logout(request)
    return HttpResponseRedirect(reverse_lazy('recruit:home'))


class LoginView(FormView):
    """login view"""

    form_class = LoginForm
    success_url = reverse_lazy('recruit:profile')
    template_name = 'recruit/login.html'

    def form_valid(self, form):
        """ process user login"""
        credentials = form.cleaned_data

        user = authenticate(username=credentials['email'],
                            password=credentials['password'])

        if user is not None:
            login(self.request, user)
            return HttpResponseRedirect(self.success_url)

        else:
            messages.add_message(self.request, messages.INFO, 'Wrong credentials\
                                please try again')
            return HttpResponseRedirect(reverse_lazy('recruit:login'))



@login_required
def update_p(request, id):
    profile = User.objects.get(id=id)
    email = profile.email
    if profile.type == 'PLAYER':
        user = PlayerMore.objects.get(email=email)
        form = CreatePlayer(request.POST or None, instance=user)

    else:
        user= CoachMore.objects.get(email=email)
        form = CreateCoach(request.POST or None, instance=user)

    if form.is_valid():
        form.save()
        return redirect('recruit:profile')
    return render(request, 'recruit/profileform.html', {'form':form, 'profile':profile})


def delete_p(request, id):
    profile = User.objects.get(id=id)

    if request.method == 'POST':
        profile.delete()
        return redirect('recruit:home')

    return render(request, 'recruit/profiledelete.html', {'profile': profile})
