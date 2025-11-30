from django import forms

from .models import Article, Developer


class DeveloperForm(forms.ModelForm):
    skills = forms.CharField(
        required=False,
        help_text='Separar por virgula',
        widget=forms.TextInput(attrs={'placeholder': 'Python, Django, React'}),
        label='Skills',
    )

    class Meta:
        model = Developer
        fields = ['name', 'email', 'seniority', 'skills']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk and self.instance.skills:
            self.initial['skills'] = ', '.join(self.instance.skills)
        self.fields['name'].label = 'Nome'
        self.fields['email'].label = 'E-mail'
        self.fields['seniority'].label = 'Senioridade'
        for field in self.fields.values():
            css = field.widget.attrs.get('class', '')
            field.widget.attrs['class'] = f'{css} w-full border border-slate-300 px-3 py-2 rounded'

    def clean_skills(self):
        raw = self.cleaned_data.get('skills', '')
        if not raw:
            return []
        parts = [part.strip() for part in raw.split(',') if part.strip()]
        return parts


class ArticleForm(forms.ModelForm):
    published_at = forms.DateTimeField(
        required=False,
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        label='Data de publicacao',
    )

    class Meta:
        model = Article
        fields = ['title', 'slug', 'content', 'published_at', 'cover_image', 'developers']
        widgets = {
            'developers': forms.CheckboxSelectMultiple,
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user is not None:
            self.fields['developers'].queryset = Developer.objects.order_by('name')
        self.fields['slug'].required = False
        self.fields['slug'].label = 'URL amigavel'
        self.fields['slug'].help_text = 'Opcional: deixe vazio para gerar automaticamente a partir do titulo'
        self.fields['title'].label = 'Titulo'
        self.fields['content'].label = 'Conteudo'
        self.fields['cover_image'].label = 'Imagem de capa (opcional)'
        self.fields['developers'].label = 'Desenvolvedores'
        if self.instance and self.instance.pk and self.instance.published_at:
            self.initial['published_at'] = self.instance.published_at.strftime('%Y-%m-%dT%H:%M')
        for field in self.fields.values():
            css = field.widget.attrs.get('class', '')
            field.widget.attrs['class'] = f'{css} w-full border border-slate-300 px-3 py-2 rounded'
