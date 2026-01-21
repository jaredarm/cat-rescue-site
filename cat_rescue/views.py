from django.shortcuts import render

def index(request):
    return render(request, "index.html")

def cats(request):
    return render(request, "cats.html")

def about(request):
    return render(request, "about.html")

def our_team(request):
    return render(request, "our_team.html")

def our_vets(request):
    return render(request, "our_vets.html")

def how_you_can_help(request):
    return render(request, "how_you_can_help.html")

def fundraising_events(request):
    return render(request, "fundraising_events.html")

def our_supporters(request):
    return render(request, "our_supporters.html")

