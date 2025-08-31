from django import forms
from .models import Supplement

class SupplementModelForm(forms.ModelForm):
    class Meta:
        model = Supplement
        fields = '__all__'

    def clean_value(self):
        price = self.cleaned_data.get('price')
        
        if price is not None and price < 2:
            self.add_error('price', 'Valor mínimo do suplemento é 2 reais.')
        
        if price <= 0:
            self.add_error('price', 'O preço deve ser um valor positivo.')

        return price

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if name and len(name) < 3:
            self.add_error('name', 'O nome do suplemento deve ter pelo menos 3 caracteres.')
        return name

    def clean_description(self):
        description = self.cleaned_data.get('description')
        if description and len(description) < 10:
            self.add_error('description', 'A descrição deve ter pelo menos 10 caracteres.')
        return description
