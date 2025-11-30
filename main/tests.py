from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from .forms import ArticleForm
from .models import Article, Developer
from django.core.exceptions import PermissionDenied


class DeveloperListViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='alice', password='pass123')
        self.other_user = User.objects.create_user(username='bob', password='pass123')
        self.dev_python = Developer.objects.create(
            user=self.user,
            name='Ana Python',
            email='ana@example.com',
            seniority='jr',
            skills=['python', 'django'],
        )
        self.dev_front = Developer.objects.create(
            user=self.user,
            name='Bruno Front',
            email='bruno@example.com',
            seniority='sr',
            skills=['react'],
        )
        Developer.objects.create(
            user=self.other_user,
            name='Outro Dev',
            email='other@example.com',
            seniority='pl',
        )

    def test_lists_all_developers(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('main:developer_list'))
        developers = list(response.context['developers'])
        self.assertEqual(developers, sorted(developers, key=lambda d: d.name))
        self.assertEqual(len(developers), 3)

    def test_filter_by_skill(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('main:developer_list'), {'skill': 'python'})
        content = response.content.decode()
        self.assertIn(self.dev_python.name, content)
        self.assertNotIn(self.dev_front.name, content)


class ArticleTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='alice', password='pass123')
        self.other_user = User.objects.create_user(username='bob', password='pass123')
        self.dev = Developer.objects.create(
            user=self.user,
            name='Ana Python',
            email='ana@example.com',
            seniority='jr',
            skills=['python'],
        )

    def test_slug_is_unique_per_user(self):
        article_one = Article.objects.create(user=self.user, title='Meu Artigo', content='primeiro')
        article_two = Article.objects.create(user=self.user, title='Meu Artigo', content='segundo')
        self.assertNotEqual(article_one.slug, article_two.slug)

        other_article = Article.objects.create(user=self.other_user, title='Meu Artigo', content='terceiro')
        self.assertEqual(other_article.slug, 'meu-artigo')

    def test_article_list_filters_by_developer(self):
        article_a = Article.objects.create(user=self.user, title='Com Ana', content='one')
        article_a.developers.add(self.dev)
        Article.objects.create(user=self.user, title='Sem Dev', content='two')

        self.client.force_login(self.user)
        response = self.client.get(reverse('main:article_list'), {'developer': self.dev.id})
        html = response.content.decode()
        self.assertIn(article_a.title, html)
        self.assertNotIn('Sem Dev', html)

    def test_update_requires_superuser(self):
        article = Article.objects.create(user=self.other_user, title='De outro', content='two')
        self.client.force_login(self.user)
        response = self.client.get(reverse('main:article_update', args=[article.pk]))
        self.assertEqual(response.status_code, 403)

        admin = User.objects.create_superuser(username='admin', password='pass123', email='admin@example.com')
        self.client.force_login(admin)
        response = self.client.get(reverse('main:article_update', args=[article.pk]))
        self.assertEqual(response.status_code, 200)

    def test_owner_can_update(self):
        article = Article.objects.create(user=self.user, title='Meu', content='two')
        self.client.force_login(self.user)
        response = self.client.get(reverse('main:article_update', args=[article.pk]))
        self.assertEqual(response.status_code, 200)

    def test_list_shows_other_users_articles(self):
        Article.objects.create(user=self.user, title='Meu', content='one')
        other_article = Article.objects.create(user=self.other_user, title='De outro', content='two')

        self.client.force_login(self.user)
        response = self.client.get(reverse('main:article_list'))
        html = response.content.decode()
        self.assertIn(other_article.title, html)

    def test_detail_visible_to_any_user(self):
        article = Article.objects.create(user=self.other_user, title='Publico', content='text')
        self.client.force_login(self.user)
        response = self.client.get(reverse('main:article_detail', args=[article.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertIn(article.title, response.content.decode())


class ArticleFormTests(TestCase):
    def test_developers_queryset_includes_all_users(self):
        user = User.objects.create_user(username='alice', password='pass123')
        other = User.objects.create_user(username='bob', password='pass123')
        dev_allowed = Developer.objects.create(user=user, name='Ana', email='ana@example.com', seniority='jr')
        dev_other = Developer.objects.create(user=other, name='Bob', email='bob@example.com', seniority='sr')

        form = ArticleForm(user=user)
        self.assertIn(dev_allowed, form.fields['developers'].queryset)
        self.assertIn(dev_other, form.fields['developers'].queryset)
        self.assertEqual(form.fields['developers'].queryset.count(), 2)
