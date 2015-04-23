import forms
import models
# modal format for 
# CLOUDS PAGE
def cloud_modals(request):
    return  [{'id':'create_UI_Project', 'action':'/create/UIProject', 
              'title':'Create Project', 'form':forms.CreateUIProject(request)},
             {'id':'delete_UI_Project', 'action':'/delete/UIProject', 
              'title':'Delete Project', 'form':forms.DeleteUIProject(request)},
             {'id':'add_Cluster_Project', 'action':'/create/ClusterProject', 
              'title':'Add Cluster Project', 'form':forms.CreateClusterProject(request)},
             {'id':'delete_Cluster_Project', 'action':'/delete/ClusterProject', 
              'title':'Delete Cluster Project', 'form':forms.DeleteClusterProject(request)},
             {'id':'createVM', 'title':'Create VM', 'form':forms.CreateVM()},
             {'id':'deleteVM', 'action':'/delete/Cluster', 
              'title':'Delete VM', 'form':forms.DeleteVM()},
            ]
