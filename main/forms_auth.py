from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django import forms


class SignupForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Nome de usuario'
        self.fields['username'].help_text = 'Obrigatorio. 150 caracteres ou menos. Use letras, numeros e @/./+/-/_.'
        self.fields['password1'].label = 'Senha'
        self.fields['password2'].label = 'Confirme a senha'
        self.fields['password1'].help_text = 'Use pelo menos 8 caracteres e evite dados pessoais ou senhas comuns.'
        self.fields['password2'].help_text = 'Repita a mesma senha para confirmar.'
        for field in self.fields.values():
            css = field.widget.attrs.get('class', '')
            field.widget.attrs['class'] = f'{css} w-full border border-slate-300 px-3 py-2 rounded'


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Nome de usuario'
        self.fields['password'].label = 'Senha'
        for field in self.fields.values():
            field.help_text = ''
        for field in self.fields.values():
            css = field.widget.attrs.get('class', '')
            field.widget.attrs['class'] = f'{css} w-full border border-slate-300 px-3 py-2 rounded'
