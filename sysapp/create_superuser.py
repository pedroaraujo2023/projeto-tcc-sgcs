# create_superuser.py
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Cria um superusuário padrão para ambiente de produção'

    def handle(self, *args, **kwargs):
        User = get_user_model()

        matricula = '100'
        senha = 'adm321'
        nome = 'Admin'
        sobrenome = 'Super'
        nome_usuario = 'superadmin'
        email = 'superadmin@email.com'

        User.objects.create_superuser(matricula=matricula, password=senha, nome=nome, sobrenome=sobrenome, nome_usuario=nome_usuario, email=email)

        self.stdout.write(self.style.SUCCESS('Superusuário criado com sucesso!'))
