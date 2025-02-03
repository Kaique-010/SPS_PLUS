from django.shortcuts import render
from django.urls import reverse_lazy
from Ordemservico.models import Ordemservico
from Ordemservico.forms import OrdemservicoForm
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView



def OS_view(request):
    os_list = Ordemservico.objects.all() 
    return render(request, 'os.html', {'os': os_list}) 



class OsCreateView(CreateView):
    model = Ordemservico
    template_name = 'os_form.html'
    form_class = OrdemservicoForm
    success_url = reverse_lazy('os.html')