from django import forms
from django.contrib.auth import get_user_model
from .models import Listing, Comment, CommonProfile, StoreProfile

User = get_user_model()


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


class UserProfileForm(forms.ModelForm):
    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(render_value=False),
        help_text='Deixe vazio para manter a senha atual.'
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'profile_picture', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password')
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user


class CommonProfileForm(forms.ModelForm):
    class Meta:
        model = CommonProfile
        fields = ['cpf']


class StoreProfileForm(forms.ModelForm):
    class Meta:
        model = StoreProfile
        fields = ['cnpj', 'razao_social']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'comment-input',
                'placeholder': 'Escreva seu comentário...',
                'rows': 4,
            }),
        }
