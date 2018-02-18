from django.shortcuts import render, redirect
from organizer.form import OrganizerSignupForm
# Create your views here.
from organizer.models import Organizer


def organizers_page(request):
    all_organizers=Organizer.objects.all()
    return render(request,'organizer/organizers_page.html',{'all_organizers':all_organizers})


def signup(request):
    if request.method=='POST':
        form=OrganizerSignupForm(request.POST)
        if form.is_valid():
            current_organizer=form.save()
            return redirect('organizer:home',current_organizer.id)
    else:
         form=OrganizerSignupForm()
    return render(request,'organizer/signup.html',{'form':form})


def home(request,organizer_id):
    current_organizer=Organizer.objects.get(id=organizer_id)
    return render(request,'organizer/home.html',{'current_organizer':current_organizer})

def view_profile(request,organizer_id):
    current_organizer=Organizer.objects.get(id=organizer_id)
    return render(request, 'organizer/profile/view_profile.html', {'current_organizer': current_organizer})

def edit_profile(request,organizer_id):
    
    current_organizer=Organizer.objects.get(id=organizer_id)
    return render(request, 'organizer/profile/edit_profile.html', {'current_organizer': current_organizer})
