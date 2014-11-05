from django.shortcuts import render
from django.http import HttpResponse


def login(request):
	return render(request, 'login.html', {'OCXlogin': 'OCX login.'})

def create_user(request):
	return render(request, 'create_user.html', {'register': 'create new user page.'})

def projects(request):
	projects = [
		{'name':'Project1', 'desc':'This is my first project.'},
		{'name': 'Project2', 'desc':'I should have a better name.' } ]

	return render(request, 'projects.html', {'user_projects': projects})

def market(request):

	resources = [
		{'name': 'Hadoop','desc':'Hadoop as a Service', 'tag': 'service', 'icon': 'http://cdn.blog-sap.com/innovation/files/2012/09/hadoop-elephant.jpg'},
		{'name': 'Wireshark','desc':'Wireshark Appliance', 'tag': 'appliance', 'icon': 'http://halozatbiztonsag.hu/sites/default/files/WireShark_2.png'},
		{'name': 'NGINX','desc':'NGINX Loadbalancer Appliance', 'tag': 'appliance', 'icon': 'http://halozatbiztonsag.hu/sites/default/files/WireShark_2.png'},
		{'name': 'BU-Compute','desc':'BU Computing', 'tag': 'compute', 'icon': 'http://www.openstack.org/themes/openstack/images/new-icons/openstack-compute-icon.png'},
		{'name': 'HU-Storage','desc':'HU Storage', 'tag': 'storage', 'icon': 'http://openstack.org//themes/openstack/images/new-icons/openstack-object-storage-icon.png'} ]


	return render(request, 'market.html', {'market': resources})


def manage(request):
	VMs = [
		{'name': 'VM1', 'fields': {'compute':'BU-large', 'storage': 'EMC-small', 'image': 'CentOS', 'status': 'off'}},
		{'name': 'VM2', 'fields': {'compute':'HU-small', 'storage': 'HP-medium', 'image': 'Ubuntu', 'status': 'off'}} ]

	return render(request, 'manage.html', {'project_VMs': VMs})

def settings(request):
	return render(request, 'settings.html', {'settings': 'project settings page.'})
