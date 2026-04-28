from django import forms
from .models import Listing

class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['titulo', 'descricao', 'categoria', 'preco', 'tipo', 'condicao']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

        # 🚨 REGRA: PJ não pode TROCA
        if self.user.tipo == 'PJ':
            self.fields['tipo'].choices = [('VENDA', 'Venda')]

    def clean(self):
        cleaned_data = super().clean()
        tipo = cleaned_data.get('tipo')

        # 🚨 VALIDAÇÃO FINAL
        if self.user.tipo == 'PJ' and tipo == 'TROCA':
            raise forms.ValidationError("Lojas não podem criar anúncios de troca.")

        return cleaned_data