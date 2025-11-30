from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView
from django.core.exceptions import PermissionDenied
from django.db.models import Count, Q
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import ArticleForm, DeveloperForm
from .forms_auth import LoginForm, SignupForm
from .models import Article, Developer


def home_redirect(request):
    return redirect('main:developer_list')


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('main:developer_list')
    else:
        form = SignupForm()
    return render(request, 'registration/signup.html', {'form': form})


class CustomLoginView(LoginView):
    form_class = LoginForm
    template_name = 'registration/login.html'
    redirect_authenticated_user = True


class DeveloperListView(LoginRequiredMixin, ListView):
    model = Developer
    template_name = 'main/developer_list.html'
    context_object_name = 'developers'

    def get_queryset(self):
        self.search = self.request.GET.get('search', '').strip()
        self.seniority = self.request.GET.get('seniority', '').strip()
        self.skill = self.request.GET.get('skill', '').strip()

        qs = (
            Developer.objects.all()
            .annotate(article_total=Count('articles', distinct=True))
            .prefetch_related('articles')
        )

        if self.search:
            qs = qs.filter(Q(name__icontains=self.search) | Q(email__icontains=self.search))
        if self.seniority:
            qs = qs.filter(seniority=self.seniority)
        if self.skill:
            qs = qs.filter(skills__icontains=self.skill)
        return qs.order_by('name')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update(
            {
                'search': self.search,
                'seniority': self.seniority,
                'skill': self.skill,
            }
        )
        return ctx

    def get_template_names(self):
        if self.request.headers.get('HX-Request'):
            return ['main/partials/developer_cards.html']
        return [self.template_name]


class DeveloperCreateView(LoginRequiredMixin, CreateView):
    model = Developer
    form_class = DeveloperForm
    template_name = 'main/developer_form.html'
    success_url = reverse_lazy('main:developer_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class DeveloperUpdateView(LoginRequiredMixin, UpdateView):
    model = Developer
    form_class = DeveloperForm
    template_name = 'main/developer_form.html'
    success_url = reverse_lazy('main:developer_list')

    def get_queryset(self):
        return Developer.objects.filter(user=self.request.user)


class DeveloperDeleteView(LoginRequiredMixin, DeleteView):
    model = Developer
    template_name = 'main/confirm_delete.html'
    success_url = reverse_lazy('main:developer_list')
    context_object_name = 'object'

    def get_queryset(self):
        return Developer.objects.filter(user=self.request.user)


class ArticleListView(LoginRequiredMixin, ListView):
    model = Article
    template_name = 'main/article_list.html'
    context_object_name = 'articles'

    def get_queryset(self):
        self.search = self.request.GET.get('search', '').strip()
        self.developer_id = self.request.GET.get('developer', '').strip()

        qs = (
            Article.objects.all()
            .annotate(developer_total=Count('developers', distinct=True))
            .prefetch_related('developers')
            .order_by('-published_at', 'title')
        )

        if self.search:
            qs = qs.filter(Q(title__icontains=self.search) | Q(content__icontains=self.search))
        if self.developer_id and self.developer_id.isdigit():
            qs = qs.filter(developers__id=self.developer_id)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update(
            {
                'search': self.search,
                'developer_id': self.developer_id,
                'developer_options': Developer.objects.order_by('name'),
            }
        )
        return ctx


class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Article
    form_class = ArticleForm
    template_name = 'main/article_form.html'
    success_url = reverse_lazy('main:article_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ArticleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Article
    form_class = ArticleForm
    template_name = 'main/article_form.html'
    success_url = reverse_lazy('main:article_list')

    def get_queryset(self):
        return Article.objects.all()

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def test_func(self):
        obj = self.get_object()
        if self.request.user.is_superuser or obj.user == self.request.user:
            return True
        raise PermissionDenied


class ArticleDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Article
    template_name = 'main/confirm_delete.html'
    success_url = reverse_lazy('main:article_list')
    context_object_name = 'object'

    def get_queryset(self):
        return Article.objects.all()

    def test_func(self):
        obj = self.get_object()
        if self.request.user.is_superuser or obj.user == self.request.user:
            return True
        raise PermissionDenied


class ArticleDetailView(LoginRequiredMixin, DetailView):
    model = Article
    template_name = 'main/article_detail.html'
    context_object_name = 'article'

    def get_queryset(self):
        return Article.objects.select_related('user').prefetch_related('developers')
