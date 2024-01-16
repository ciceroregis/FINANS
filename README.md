# Finans
## Projeto Financeiro Pessoal

Este é um aplicativo de gerenciamento financeiro construído com o framework Django. Ele permite que os usuários registrem suas despesas e receitas, estabeleçam orçamentos e metas financeiras, acompanhem suas carteiras de investimentos e muito mais.

## Recursos
- Registro de despesas e receitas
- Integração com contas bancárias e cartões de crédito ## a fazer
- Acesso via aplicativo móvel ou plataforma web   ## a fazer

## Tecnologias utilizadas
- asgiref>=3.7.2
- autopep8>=2.0.4
- Django>=5.0
- django-appconf>=1.0.6
- django-crispy-forms>=2.1
- django-environ>=0.11.2
- django-model-utils>=4.3.1
- django-notifications-hq>=1.7.0
- django-rename-app>=0.1.7
- django-select2>=8.1.2
- filebrowser>=1.1.4
- gunicorn>=21.2.0
- Jinja2>=3.1.2
- jsonfield>=3.1.0
- MarkupSafe>=2.1.3
- packaging>=23.2
- Pillow>=10.1.0
- pycodestyle>=2.11.1
- python-slugify>=8.0.1
- pytz>=2023.3.post1
- requests>=2.31.0
- self>=2020.12.3
- six>=1.16.0
- sqlparse>=0.4.4
- swapper>=1.3.0
- text-unidecode>=1.3
- toml>=0.10.2
- tzdata>=2023.3
- urllib3>=2.1.0
- whitenoise>=6.6.0
- mysqlclient>=2.2.0
- crispy>=0.7.4


    
## Como usar
1. Faça o clone deste repositório  `https://gitlab.com/cicero.cruz/finans`
2. Crie um virtualenv e instale as dependências listadas no arquivo `requirements.txt`
3. Execute as migrações do banco de dados: `python manage.py makemigrations` e `python manage.py migrate`
4. Inicie o servidor: `python manage.py runserver`
5. Acesse o aplicativo através do endereço `http://localhost:8000/`



