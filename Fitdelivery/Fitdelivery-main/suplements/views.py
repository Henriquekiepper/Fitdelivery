from django.shortcuts import render, redirect
from django.http import HttpResponse
from suplements.models import Supplement
from suplements.forms import SupplementModelForm
from django.views import View
from django.views.generic import ListView, CreateView,DetailView,UpdateView


""""
def new_supplement_view(request):
    if request.method == 'POST':
        new_supplement_form = SupplementModelForm(request.POST, request.FILES)
        if new_supplement_form.is_valid():
            new_supplement_form.save()
            return redirect('supplement_list')

    else:
        new_supplement_form = SupplementModelForm()
    return render(request, 
                  'new_supplement.html',
                  {'new_supplement_form':new_supplement_form})
"""""""
class SupplementView(View):

    def get(self,request):
        supplements = Supplement.objects.all().order_by('name')
        search = request.GET.get('search')
        if search:
            supplements = Supplement.objects.filter(category__name__icontains=search)

        return render( request,
                  'supplements.html',
                  {'supplements':supplements})
    """


class SupplementListView(ListView):
    model = Supplement
    template_name = 'supplements.html'
    context_object_name = 'supplements'

    def get_queryset(self):
        search = self.request.GET.get('search')
        if search:
            return Supplement.objects.filter(name__icontains=search)
        return Supplement.objects.all().order_by('name')

"""
class NewSupplementView(View):

    def get(self,request):
        new_supplement_form = SupplementModelForm()
        return render(request, 'new_supplement.html',{'new_supplement_form': new_supplement_form})
    
    def post(self,request):
        new_supplement_form = SupplementModelForm(request.POST, request.FILES)
        if new_supplement_form.is_valid():
            new_supplement_form.save()
            return redirect('supplement_list')
        return render(request, 'new_supplement.html',{'new_supplement_form': new_supplement_form})
"""
class NewSupplementCreateView(CreateView):
    model = Supplement
    form_class= SupplementModelForm
    template_name = 'new_supplement.html'
    success_url = '/supplements/'


class SupplementDetailView(DetailView):
    model = Supplement
    template_name = 'supplement_detail.html'

class SupplementUpdateView(UpdateView):
    model = Supplement
    form_class = SupplementModelForm
    template_name = 'supplement_update.html'
    success_url = '/supplements/'

