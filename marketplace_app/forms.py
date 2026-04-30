from django import forms
from .models import Listing


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class ListingForm(forms.ModelForm):

    image = forms.ImageField(
        required=False,
        help_text='Selecione uma imagem para o anúncio.'
    )

    class Meta:
        model = Listing
        fields = [
            'title',
            'description',
            'price',
            'category',
            'listing_type',
            'condition',
        ]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # Se for loja, remove opção "Troca"
        if self.user and self.user.is_store:
            self.fields['listing_type'].choices = [
                ('sale', 'Venda')
            ]