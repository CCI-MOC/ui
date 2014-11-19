from django.shortcuts import render
from django.http import HttpResponse
import ui_api as api

def login(request):
	return render(request, 'login.html', {'OCXlogin': 'OCXi'})

def create_user(request):
	return render(request, 'create_user.html', {'register': 'create new user page.'})

def projects(request):

	# similar to manage, projects will have to pull data of current projects on the deployment
	# projects = keystone.<projects>.list()
	# projects.html will have to change to reflect data from received projects
	# when a project is selected from this list, relevant info will be passed to the 
	# project management page, for access to nova

	projects = [
		{'name':'Project1', 'desc':'This is my first project.'},
		{'name':'Project2', 'desc':'I should have a better name.'} ]

	return render(request, 'projects.html', {'user_projects': projects})

def market(request):

	resources = [
		{'name': 'Hadoop','desc':'Hadoop as a Service', 'tag': 'service', 'icon': 'http://cdn.blog-sap.com/innovation/files/2012/09/hadoop-elephant.jpg'},
		{'name': 'Wireshark','desc':'Wireshark Appliance', 'tag': 'appliance', 'icon': 'http://halozatbiztonsag.hu/sites/default/files/WireShark_2.png'},
		{'name': 'NGINX','desc':'NGINX Loadbalancer Appliance', 'tag': 'appliance', 'icon': 'http://shailan.com/wp-content/uploads/nginx-logo-1.png'},
		{'name': 'BU-Compute','desc':'BU Computing', 'tag': 'compute', 'icon': 'http://www.openstack.org/themes/openstack/images/new-icons/openstack-compute-icon.png'},
		{'name': 'HU-Storage','desc':'HU Storage', 'tag': 'storage', 'icon': 'http://openstack.org//themes/openstack/images/new-icons/openstack-object-storage-icon.png'} ]


	return render(request, 'market.html', {'market': resources})


def manage(request):
	# VMs should receive data from a call to nova.servers.list( w/ details of each instance )
	# 'nova' is based off a specific project / client
	# e.g. nova = Client('2', 'nova', 'admin', 'service', 'http://10.0.2.15:5000/v2.0')
	# depending on the object of each instance, template code (manage.html) has to change
	VMs = api.list()

	hard_code =  [
		{'name': 'VM1', 'desc': 'My small VM', 'fields': {'compute':'BU-small', 'network': 'pubNet1', 'storage': 'EMC-small', 'image': 'CentOS', 'status': 'off'}},
		{'name': 'VM2', 'desc': 'My larger VM', 'fields': {'compute':'HU-large', 'network': 'privNet1', 'storage': 'HP-medium', 'image': 'Ubuntu', 'status': 'off'}} ]

	return render(request, 'manage.html', {'project_VMs': VMs})

def settings(request):
	return render(request, 'settings.html', {'settings': 'project settings page.'})

def modal(request):

	options = [
		{'compute': 'small'},
		{'storage': 'BU'},
		{'network': 'private'}]

	return render(request, 'modal.html', {'options': options})
