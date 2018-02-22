from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.shortcuts import render, redirect
from organizer.form import OrganizerSignupForm, OrganizerProfileForm
# Create your views here.
from organizer.models import Organizer
from django.views.generic import *
from .filters import OrganizerFilter


class OrganizerBrowseView(ListView):
    model = Organizer
    context_object_name = 'all_organizers'
    template_name = 'organizer/browse_organizer.html'


def search_organizers(request):
    try:
        organizer = Organizer.objects.get(pk=request.user.id)
    except Exception:
        organizer = None
    organizers = Organizer.objects.all()
    organizers_filter = OrganizerFilter(request.GET, queryset=organizers)
    context = {'O': organizer, 'filter': organizers_filter}
    return render(request, 'organizer/browse_organizer.html', context)



def organizers_page(request):
    all_organizers=Organizer.objects.all()
    return render(request,'organizer/organizers_page.html',{'all_organizers' : all_organizers})


def signup(request):
    if request.method=='POST':
        form=OrganizerSignupForm(request.POST)
        if form.is_valid():
            current_organizer=form.save()
            return redirect('organizer:home')
    else:
         form=OrganizerSignupForm()
    return render(request,'organizer/signup.html',{'form':form})


def home(request):
    try:
        o = Organizer.objects.get(pk=request.user.id)
        context = {'O': o}
        return render(request, 'organizer/home.html', context)
    except Exception:
        return redirect('organizer:login')



def view_profile(request):
    if request.user.username:
        user = Organizer.objects.get(pk=request.user)
        # player = vars(user) to list all attributes
        organizer = user.profile()
        context = {'organizer': organizer}
        return render(request, 'organizer/profile/view_profile.html', context)
    else:
        return redirect('organizer:login')


def edit_profile(request):
    if request.user.username:
        organizer = Organizer.objects.get(pk=request.user.id)
        if request.method == 'POST':
            form = OrganizerProfileForm(request.POST, instance=organizer)
            if form.is_valid():
                form.save()
                return redirect('organizer:view_profile')
        else:
            form = OrganizerProfileForm(instance=organizer)
            context = {'form': form}
            return render(request, 'organizer/profile/edit_profile.html', context)
    else:
        return redirect('organizer:login')


def Org_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('organizer:home',)
    return render(request, 'organizer/login.html')


def Org_logout(request):
    logout(request)
    return redirect('organizer:organizers_page')

def organizer_change_password(request):
    if request.user.username:
        if request.method == 'POST':
            form = PasswordChangeForm(data=request.POST, user=request.user)
            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request, user)
                return redirect('organizer:home')
            else:
                messages.error(request, 'Please correct the error below.')
                return redirect('organizer:change_password')
        else:
            form = PasswordChangeForm(user=request.user)
            return render(request, 'organizer/change_password.html', {'form': form})
    else:
        return redirect('organizer:login')


