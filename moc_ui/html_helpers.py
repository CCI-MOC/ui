import forms
# modal format for 
# PROJECTS PAGE
def project_modals(request):
    return  [{'id':'create_UI_Project', 'action':'/create/UIProject', 
              'title':'Create Project', 'form':forms.UIProject()},
             {'id':'delete_UI_Project', 'action':'/delete/UIProject', 
              'title':'Delete Project', 'form':forms.UIProject()},
             # {'id':'create_UI_Project', 'action':'/create/UIProject', 
             #  'title':'Create Project', 'form':forms.CreateUIProject(request)},
             # {'id':'delete_UI_Project', 'action':'/delete/UIProject', 
             #  'title':'Delete Project', 'form':forms.DeleteUIProject(request)},
             {'id':'add_Cluster_Project', 'action':'/create/ClusterProject', 
             {'id':'add_Cluster_Project', 'action':'/create/ClusterProject', 
              'title':'Add Cluster Project', 'form':forms.ClusterProject()},
             {'id':'delete_Cluster_Project', 'action':'/delete/ClusterProject', 
              'title':'Delete Cluster Project', 'form':forms.ClusterProject()},
            ]
# CONTROL (VM) PAGE
def vm_modals(request):
    return [ {'id':'createVM', 'title':'Create VM', 'form':forms.CreateVM()},
             {'id':'deleteVM', 'action':'/delete/Cluster', 
              'title':'Delete VM', 'form':forms.DeleteVM()},

            ]
