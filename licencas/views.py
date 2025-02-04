from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from .models import Licencas, Filiais, Empresas
from .forms import LicencasForm, EmpresasForm, FiliaisForm


class LicencasListView(ListView):
    model = Licencas
    template_name = "licencas/licencas_list.html"
    context_object_name = "licencas"


class LicencasCreateView(CreateView):
    model = Licencas
    form_class = LicencasForm
    template_name = "licencas/licencas_form.html"
    success_url = reverse_lazy("licencas_list")


class LicencasUpdateView(UpdateView):
    model = Licencas
    form_class = LicencasForm
    template_name = "licencas/licencas_form.html"
    success_url = reverse_lazy("licencas_list")


class LicencasDetailView(DetailView):
    model = Licencas
    template_name = "licencas/licencas_detail.html"
    context_object_name = "licenca"


class LicencasDeleteView(DeleteView):
    model = Licencas
    template_name = "licencas/licencas_confirm_delete.html"
    success_url = reverse_lazy("licencas_list")


class EmpresaListView(ListView):
    model = Empresas
    template_name = 'empresa_list.html'
    context_object_name = 'empresas'

class EmpresaCreateView(CreateView):
    model = Empresas
    form_class = EmpresasForm
    template_name = 'licencas/empresa_create.html'

class EmpresaUpdateView(UpdateView):
    model = Empresas
    form_class = EmpresasForm
    template_name = 'licencas/empresa_update.html'

class EmpresaDetailView(DetailView):
    model = Empresas
    template_name = 'licencas/empresa_detail.html'

class EmpresaDeleteView(DeleteView):
    model = Empresas
    template_name = 'licencas/empresa_confirm_delete.html'
    success_url = reverse_lazy('empresa_list')

class FilialListView(ListView):
    model = Filiais
    template_name = 'filial_list.html'
    context_object_name = 'filiais'

class FilialCreateView(CreateView):
    model = Filiais
    form_class = FiliaisForm
    template_name = 'licencas/filial_create.html'

class FilialUpdateView(UpdateView):
    model = Filiais
    form_class = FiliaisForm
    template_name = 'licencas/filial_update.html'

class FilialDetailView(DetailView):
    model = Filiais
    template_name = 'licencas/filial_detail.html'

class FilialDeleteView(DeleteView):
    model = Filiais
    template_name = 'licencas/filial_confirm_delete.html'
    success_url = reverse_lazy('filial_list')