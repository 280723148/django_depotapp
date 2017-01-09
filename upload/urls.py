from django.conf.urls import url
from views import UploadRolesFormView

urlpatterns =[
    url(r'^upload/$', UploadRolesFormView.as_view(), name='rolesUpload'),
]
