# Create your views here.
from django.views.generic.edit import FormView, CreateView
from django.views.decorators.csrf import csrf_exempt
from django.core.urlresolvers import reverse_lazy
from .models import Roles


class UploadRolesFormView(CreateView):
    template_name = 'upload_roles.html'
    model = Roles
    fields = ['name', 'tasks', 'vars']
    success_url = reverse_lazy('app:index')

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(UploadRolesFormView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super(UploadRolesFormView, self).form_valid(form)
