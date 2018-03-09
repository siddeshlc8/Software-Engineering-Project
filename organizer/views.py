from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.shortcuts import render, redirect
from organizer.form import  OrganizerProfileForm
# Create your views here.
from organizer.models import Organizer


def home(request):
    try:
        Organizer.objects.get(pk=request.user.id)
        return render(request, 'organizer/home.html')
    except Exception:
        return redirect('login')


def view_profile(request):
    if request.user.username:
        user = Organizer.objects.get(pk=request.user)
        # player = vars(user) to list all attributes
        organizer = user.profile()
        context = {'organizer': organizer}
        return render(request, 'organizer//view_profile.html', context)
    else:
        return redirect('login')


def edit_profile(request):
    if request.user.username:
        organizer = Organizer.objects.get(pk=request.user.id)
        if request.method == 'POST':
            form = OrganizerProfileForm(request.POST, instance=organizer)
            if form.is_valid():
                form.save()
                messages.success(request, 'You have  successfully edited your profile!')
                return redirect('organizer:view_profile')
        else:
            form = OrganizerProfileForm(instance=organizer)
            context = {'form': form}
            return render(request, 'organizer/edit_profile.html', context)
    else:
        return redirect('login')


def organizer_change_password(request):
    if request.user.username:
        if request.method == 'POST':
            form = PasswordChangeForm(data=request.POST, user=request.user)
            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'You have  successfully changed your password!')
                return redirect('organizer:home')
            else:
                messages.error(request, 'Please correct the error below.')
                return redirect('organizer:change_password')
        else:
            form = PasswordChangeForm(user=request.user)
            return render(request, 'organizer/change_password.html', {'form': form})
    else:
        return redirect('login')


