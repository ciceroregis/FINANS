# Finans
## Projeto Financeiro Pessoal

Este é um aplicativo de gerenciamento financeiro construído com o framework Django. Ele permite que os usuários registrem suas despesas e receitas, estabeleçam orçamentos e metas financeiras, acompanhem suas carteiras de investimentos e muito mais.

## Recursos
- Registro de despesas e receitas
- Integração com contas bancárias e cartões de crédito ## a fazer
- Acesso via aplicativo móvel ou plataforma web   ## a fazer

## Tecnologias utilizadas
- django==4.1
- autopep8==1.6.0
- dj-database-url==0.5.0
- gunicorn==20.1.0
- pycodestyle==2.8.0
- pytz==2021.3
- sqlparse==0.4.2
- toml==0.10.2
- whitenoise==5.3.0
- django-environ==0.8.1
- psycopg2==2.9.3
- django-filebrowser-no-grappelli==4.0.1
- django-colorfield==0.7.2


    
## Como usar
1. Faça o clone deste repositório  `https://gitlab.com/cicero.cruz/finans`
2. Crie um virtualenv e instale as dependências listadas no arquivo `requirements.txt`
3. Execute as migrações do banco de dados: `python manage.py makemigrations` e `python manage.py migrate`
4. Inicie o servidor: `python manage.py runserver`
5. Acesse o aplicativo através do endereço `http://localhost:8000/`



