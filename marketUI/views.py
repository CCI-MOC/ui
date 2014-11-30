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
			image = form.cleaned_data['imageName']
			flavor = form.cleaned_data['flavorName']
			return HttpResponseRedirect('/project_space/manage/create/'+VMname+';'+image+';'+flavor)
	else:
		VMs = api.listVMs()
		images = api.listImages()
		flavors = api.listFlavors()
		tenant = api.getTenant()
		return render(request, 'manage.html', 
		{'project_VMs':VMs, 'images':images, 'flavors':flavors, 'tenant':tenant.name})

def deleteVM(request, VMname):
	api.delete(VMname)
	time.sleep(8)
	return HttpResponseRedirect('/project_space/manage')

def createVM(request, VMname, imageName, flavorName):
        api.createVM(VMname, imageName, flavorName)
        time.sleep(15)
        return HttpResponseRedirect('/project_space/manage')

def createDefaultVM(request, VMname):
	api.createDefault(VMname)
	time.sleep(15)
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
