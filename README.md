## Open Cloud Exchange interface
An alternative OpenStack Dashboard to Horizon for the MOC.

###Setup and Usage
---

####1. Clone repo
* git clone https://github.com/CCI-MOC/ui.git 

####2. Start Django Project
* create python virtual enviornment using "virtualenv [env-name]"
* source environment using "source [env-name]/bin/activate"
* install requirements using "pip install -r"
* create database with "./syncdb" - creating django admin is unneccessary, not currently using
* create folder to hold session ids with "mkdir session"
* run server with "./runserver"

####3. Interface Usage

* point browser to localhost:8000
* register as a new user using your openstack credentials

#####Login Page

* login as an existing keystone user, or register with keystone
  * a project admin must add user to project for that user to gain access;
  * or a new user can create a project, and will join that project as an admin

#####Projects Page

* enter a project or create a new project
  * attempts to create keystone, nova, glance clients for user in project (username, password, project)

#####Project Management

* create/edit/delete VMs
  * selection of a VM allows for control (start, stop) and resizing (incomplete functionality; needs resize confirmation/revert)
  * create VM with available flavors, images
  * access/use active VMs via VNC

#####Project Settings

* add/edit current project's users; ADMIN ONLY
  * add users to project
  * edit users' roles
  * delete current project

#####Marketplace

* faked data; example for future implementation

###TODO, FAQ, Issues
---

#####TODO

* State DB - checking users, endpoints, session info
* With a State DB:
  * Improvement of Keystone client sessions
  * Currently inefficient
  * Some privilege workarounds may be solved using private keystone endpoint, port 353572 (instead of public 5000)
* Add error checking
* Implement OCX Library

#####Known Issues

* Refer to outstanding issues

#####FAQ

* Why does the UI not work anymore? 
  * Run ./rejoin**stack.sh

* Why does OpenStack send connection errors? 
  * You might need to rejoin or restack 

* Why does Django say port already in use when running server?
  * OpenStack may be using the port, either runserver first, or specify port (ie. python manage.py runserver 9999)

* How can I test the OpenStack python API effeciently??
  * Look at UI/marketUI/auth.py. Use the defined keystone, glance and nova clients via python command line (first run 'source ~/devstack/openrc')

