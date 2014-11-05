from django.shortcuts import render
from django.http import HttpResponse


def login(request):
	return render(request, 'login.html', {'OCXlogin': 'OCX login.'})

def create_user(request):
	return render(request, 'create_user.html', {'register': 'create new user page.'})

def projects(request):
	projects = [{'name':'Project1', 'desc':'This is my first project.'}, 
	{'name': 'Project2', 'desc':'I should have a better name.' }]

	return render(request, 'projects.html', {'user_projects': projects})

def market(request):
	return render(request, 'market.html', {'market': 'marketplace page.'})

def manage(request):
	return render(request, 'manage.html', {'manage': 'project management page.'})

def settings(request):
	return render(request, 'settings.html', {'settings': 'project settings page.'})

