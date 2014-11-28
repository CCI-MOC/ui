from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
import ui_api as api
import time
from forms import NameForm

def login(request):
	return render(request, 'login.html', {'OCXlogin': 'OCXi'})

def create_user(request):
	return render(request, 'create_user.html', {'register': 'create new user page.'})

def projects(request):

	projects = api.listTenants()	

	#projects = [
	#	{'name':'Project1', 'desc':'This is my first project.'},
	#	{'name':'Project2', 'desc':'I should have a better name.'} ]

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
	if request.method == 'POST':
		form = NameForm(request.POST)
		if form.is_valid():
			VMname = form.cleaned_data['newVM']
			return HttpResponseRedirect('/project_space/manage/create/'+VMname)
	else:
		VMs = api.listVMs()
		tenant = api.getTenant()
		return render(request, 'manage.html', {'project_VMs': VMs, 'tenant': tenant.name})

def deleteVM(request, VMname):
	api.delete(VMname)
	time.sleep(5)
	#VMs = api.listVMs()	
	#return render(request, 'manage.html', {'project_VMs': VMs})
	return HttpResponseRedirect('/project_space/manage')

def createDefaultVM(request, VMname):
	api.createDefault(VMname)
	time.sleep(10)
	return HttpResponseRedirect('/project_space/manage')

def settings(request):
	tenant = api.getTenant()	
	users = api.listUsers(tenant)
	return render(request, 'settings.html', {'tenant': tenant.name, 'users': users})

def modal(request):
	options = [
		{'compute': 'small'},
		{'storage': 'BU'},
		{'network': 'private'}]

	return render(request, 'modal.html', {'options': options})
