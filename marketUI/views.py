from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
import ui_api as api
import time
from forms import NameForm, EditForm, ControlForm, LoginForm, TenantLoginForm

def login(request):
	return render(request, 'login.html', {'OCXlogin': 'OCXi'})

def create_user(request):
	return render(request, 'create_user.html', {'register': 'create new user page.'})

def projects(request):
        if request.method == 'POST':
                form = LoginForm(request.POST)
                if form.is_valid():
                        username = form.cleaned_data['username']
                        password = form.cleaned_data['password']	
			projects = api.listTenants()	
			return render(request, 'projects.html', 
			{'user_projects': projects, 'username':username, 'password':password})
        else:
		projects = api.listTenants()	
		return render(request, 'projects.html', {'user_projects': projects})

def enterProject(request):
        if request.method == 'POST':
                form = TenantLoginForm(request.POST)
                if form.is_valid():
                        username = form.cleaned_data['username']
                        password = form.cleaned_data['password']	
                        tenantName = form.cleaned_data['tenantName']
			tenantID = form.cleaned_data['tenantID']
			if api.validUser(username, tenantID):
				api.joinTenant(username, password, tenantName)
				VMs = api.listVMs()
				images = api.listImages()
				flavors = api.listFlavors()
				tenant = api.getTenant()
				return render(request, 'manage.html', 
				{'project_VMs':VMs, 'images':images, 'flavors':flavors, 'tenant':tenant.name})
	print('Invalid User')
	return HttpResponseRedirect('/projects/')

def market(request):

	resources = [
		{'name': 'Hadoop','desc':'Hadoop as a Service', 'tag': 'service', 'icon': 'http://cdn.blog-sap.com/innovation/files/2012/09/hadoop-elephant.jpg'},
		{'name': 'Wireshark','desc':'Wireshark Appliance', 'tag': 'appliance', 'icon': 'http://halozatbiztonsag.hu/sites/default/files/WireShark_2.png'},
		{'name': 'NGINX','desc':'NGINX Loadbalancer Appliance', 'tag': 'appliance', 'icon': 'http://shailan.com/wp-content/uploads/nginx-logo-1.png'},
		{'name': 'BU-Compute','desc':'BU Computing', 'tag': 'compute', 'icon': 'http://www.openstack.org/themes/openstack/images/new-icons/openstack-compute-icon.png'},
		{'name': 'HU-Storage','desc':'HU Storage', 'tag': 'storage', 'icon': 'http://openstack.org//themes/openstack/images/new-icons/openstack-object-storage-icon.png'} ]


	return render(request, 'market.html', {'market': resources})


###Project Management Page###

def manage(request):
	if request.method == 'POST':
		form = NameForm(request.POST)
		if form.is_valid():
			VMname = form.cleaned_data['newVM']
			image = form.cleaned_data['imageName']
			flavor = form.cleaned_data['flavorName']
			return HttpResponseRedirect('/project_space/manage/create/'+VMname+';'+image+';'+flavor)	
	VMs = api.listVMs()
	images = api.listImages()
	flavors = api.listFlavors()
	tenant = api.getTenant()
	return render(request, 'manage.html', 
	{'project_VMs':VMs, 'images':images, 'flavors':flavors, 'tenant':tenant.name})

def deleteVM(request, VMname):
	api.delete(VMname)
	return HttpResponseRedirect('/project_space/manage')

def createVM(request, VMname, imageName, flavorName):
        api.createVM(VMname, imageName, flavorName)
        return HttpResponseRedirect('/project_space/manage')

def createDefaultVM(request, VMname):
	api.createDefault(VMname)
	return HttpResponseRedirect('/project_space/manage')

def edit(request):
        if request.method == 'POST':
                form = EditForm(request.POST)
                if form.is_valid():
                        VM_id = form.cleaned_data['VM_id']
                        flavor_id = form.cleaned_data['flavor_id']	
			api.editVM(VM_id, flavor_id)
			return HttpResponseRedirect('/project_space/manage')
        else:
		return HttpResponseRedirect('/project_space/manage')

def editControlVM(request):
        if request.method == 'POST':
                form = ControlForm(request.POST)
                if form.is_valid():
			VM_id = form.cleaned_data['VM_id']
			if(form.cleaned_data['action'] == 'start'):
			  api.startVM(VM_id)
			elif(form.cleaned_data['action'] == 'pause'):
			  api.pauseVM(VM_id)
			elif(form.cleaned_data['action'] == 'stop'):
			  api.stopVM(VM_id)
	return HttpResponseRedirect('/project_space/manage')

###End Project Management###


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
