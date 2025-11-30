from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify


class Developer(models.Model):
    SENIORITY_CHOICES = [
        ('jr', 'Jr'),
        ('pl', 'Pl'),
        ('sr', 'Sr'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='developers')
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    seniority = models.CharField(max_length=2, choices=SENIORITY_CHOICES)
    skills = models.JSONField(blank=True, null=True)

    def __str__(self):
        return self.name

    def articles_count(self):
        return self.articles.count()


class Article(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='articles')
    title = models.CharField(max_length=255)
    slug = models.SlugField(blank=True)
    content = models.TextField()
    published_at = models.DateTimeField(blank=True, null=True)
    cover_image = models.ImageField(upload_to='covers/', blank=True, null=True)
    developers = models.ManyToManyField(Developer, related_name='articles', blank=True)

    def __str__(self):
        return self.title

    def developers_count(self):
        return self.developers.count()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._generate_unique_slug()
        super().save(*args, **kwargs)

    def _generate_unique_slug(self):
        base_slug = slugify(self.title)[:50] or 'article'
        slug = base_slug
        counter = 1
        while Article.objects.filter(user=self.user, slug=slug).exclude(pk=self.pk).exists():
            slug = f'{base_slug}-{counter}'
            counter += 1
        return slug

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'slug'],
                name='unique_article_slug_per_user',
            )
        ]
