from django.shortcuts import HttpResponse, render


def home_page(request):
    return render(request, 'cricket/home_page.html')
