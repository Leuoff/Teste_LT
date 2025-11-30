# LT Cloud (Django)

Implementacao em Python/Django inspirada no desafio Laravel + Livewire. Stack ajustada para Django + Tailwind + HTMX (filtros em tempo quase real).

## Rodar em 6 passos
1) Virtualenv: `python -m venv venv` e ative (`venv\Scripts\activate` no Windows, `source venv/bin/activate` no Linux/macOS).
2) Dependencias: `pip install -r requirements.txt`.
3) Banco: `python manage.py migrate`.
4) (Opcional) Dados fake: `python manage.py seed_demo --users 3 --developers 12 --articles 12` (senha dos demos: `password`).
5) Admin: `python manage.py createsuperuser`.
6) Servidor: `python manage.py runserver`.

## O que tem pronto
- Auth completa (login/registro/reset).
- Desenvolvedores: CRUD, filtros HTMX em tempo real por nome/email/senioridade/skill, contagem de artigos.
- Artigos: CRUD (titulo/slug/conteudo rich-text/data/capa opcional), N:N com desenvolvedores, contagem de devs por artigo.
- UI: grid desktop / lista mobile, badges, tema claro/escuro persistente.
- Dados fake (Faker), testes automatizados, TinyMCE para conteudo.

## Politicas
- Desenvolvedores: cada usuario so edita seus proprios registros.
- Artigos: visiveis para usuarios autenticados; autor ou admin podem editar/remover.

## URLs rapidas
- Auth: `/signup/`, `/accounts/login/`, `/accounts/password_reset/`
- Devs: `/developers/`
- Artigos: `/articles/` e `/articles/<id>/`
