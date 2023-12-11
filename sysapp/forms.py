from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
from .models import Usuario, Chamado


class UsuarioForm(forms.ModelForm):
    matricula = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Matrícula'}))
    password = forms.CharField(label='Senha', widget=forms.PasswordInput)

    class Meta:
        model = Usuario
        fields = '__all__'  
  

class CustomLoginForm(AuthenticationForm):
    matricula = forms.CharField(
        label='Matrícula/Siap',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    password = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['matricula'].label = 'Matrícula/Siap'

    class Meta:
        model = Usuario
        fields = ['matricula', 'password']

    def clean(self):
        matricula = self.cleaned_data.get('matricula')
        password = self.cleaned_data.get('password')

        if matricula is not None and password:
            user = authenticate(request=self.request, username=matricula, password=password)
            
            if user is None:
                raise forms.ValidationError(
                    f'Matricula ou senha incorretas. Matricula fornecida: {matricula}',
                    code='invalid_login',
                    params={'matricula': matricula},
                )
            if user is None:
                raise forms.ValidationError('Matrícula ou senha incorretas. Matrícula fornecida: {}'.format(matricula))
            
            if not user.is_active:
                raise forms.ValidationError('Este usuário está inativo.')
            
            self.user_cache = user

        return self.cleaned_data

class ChamadoForm(forms.ModelForm):
    class Meta:
        model = Chamado
        fields = ['tipo', 'categoria', 'titulo', 'descricao', 'prioridade', 'anexo']



    class Meta:
        model = Usuario
        fields = '__all__'
      
