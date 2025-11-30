import random

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from faker import Faker

from main.models import Article, Developer


class Command(BaseCommand):
    help = "Gera dados de exemplo com Faker (usuarios, developers e artigos)."

    def add_arguments(self, parser):
        parser.add_argument('--users', type=int, default=2, help='Quantidade de usuarios demo')
        parser.add_argument('--developers', type=int, default=10, help='Quantidade de developers')
        parser.add_argument('--articles', type=int, default=10, help='Quantidade de artigos')

    def handle(self, *args, **options):
        fake = Faker('pt_BR')
        User = get_user_model()

        users = []
        for i in range(options['users']):
            username = f'demo{i+1}'
            user, _ = User.objects.get_or_create(username=username, defaults={'email': f'{username}@example.com'})
            user.set_password('password')
            user.save()
            users.append(user)
        self.stdout.write(self.style.SUCCESS(f'Criados {len(users)} usuarios (senha: password)'))

        devs = []
        for _ in range(options['developers']):
            user = random.choice(users)
            name = fake.name()
            dev = Developer.objects.create(
                user=user,
                name=name,
                email=fake.unique.email(),
                seniority=random.choice(['jr', 'pl', 'sr']),
                skills=random.sample(['python', 'django', 'react', 'docker', 'aws', 'sql'], k=random.randint(1, 4)),
            )
            devs.append(dev)
        self.stdout.write(self.style.SUCCESS(f'Criados {len(devs)} developers'))

        for _ in range(options['articles']):
            user = random.choice(users)
            title = fake.sentence(nb_words=4)
            article = Article.objects.create(
                user=user,
                title=title,
                content=fake.paragraph(nb_sentences=5),
                published_at=fake.date_time_this_year(),
            )
            chosen = random.sample(devs, k=random.randint(1, min(3, len(devs))))
            article.developers.add(*chosen)
        self.stdout.write(self.style.SUCCESS(f'Criados {options["articles"]} artigos'))
