from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin


class UsuarioManager(BaseUserManager):
    def create_user(self, matricula, password=None, siape=None, **extra_fields):
        if not matricula and not siape:
            raise ValueError('Matrícula ou SIAPE devem ser fornecidos')

        user = self.model(matricula=matricula, siape=siape, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, matricula, password=None, siape=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(matricula, password, siape, **extra_fields)

class Usuario(AbstractBaseUser, PermissionsMixin):
    USUARIO_CHOICES = [
        ('Servidor', 'Servidor'),
        ('Aluno', 'Aluno'),
    ]
    matricula = models.CharField(unique=True, max_length=50, blank=False, null=False, verbose_name='Matrícula')
    siape = models.CharField(unique=True, max_length=50, blank=True, null=True, verbose_name='SIAPE')
    nome = models.CharField(max_length=100, blank=False, null=False, verbose_name='Nome')
    sobrenome = models.CharField(max_length=100, blank=False, null=False, verbose_name='Sobrenome')
    nome_usuario = models.CharField(unique=True, max_length=100, blank=False, null=False, verbose_name='Nome de Usuário')
    email = models.EmailField(unique=True, verbose_name='E-mail')
    password = models.CharField(max_length=128,blank=False, null=False,verbose_name='Senha', default='')
    tipo_usuario = models.CharField(max_length=8, choices=USUARIO_CHOICES, default='1', verbose_name='Tipo de Usuário')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UsuarioManager()

    REQUIRED_FIELDS = ['nome', 'sobrenome', 'nome_usuario', 'email']
    USERNAME_FIELD = 'matricula'

   
    def __str__(self):
        return f"{self.nome} {self.sobrenome}"


class Chamado(models.Model):
    ESTADO_CHOICES = [
        ('Novos', 'Novos'),
        ('Em andamento', 'Em andamento'),
        ('Finalizados', 'Finalizados'),
    ]
 
    TIPO_CHOICES = [
        ('Suporte', 'Suporte'),
        ('Financeiro', 'Financeiro'),
        ('Outros', 'Outros')
    ]

    CATEGORIA_CHOICES = [
        ('Informática', 'Informática'),
        ('Redes', 'Redes'),
        ('Segurança', 'Segurança'),
        ('Outros', 'Outros'),
    ]

    PRIORIDADE_CHOICES = [
        ('Baixa', 'Baixa'),
        ('Média', 'Média'),
        ('Alta', 'Alta'),
    ]
    
    codigo = models.AutoField(primary_key=True)
    tipo = models.CharField(max_length=20, null=True, blank=False, choices=TIPO_CHOICES)
    categoria = models.CharField(max_length=20, blank=True, null=True, choices=CATEGORIA_CHOICES)
    titulo = models.CharField(max_length=255, blank=True, null=True)
    descricao = models.TextField(null=True, blank=True)
    prioridade = models.CharField(max_length=10, null=True, choices=PRIORIDADE_CHOICES)
    anexo = models.FileField(upload_to='anexos/', null=True, blank=True)

    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='Novos', verbose_name='Estado')

    # Adicione a chave estrangeira para associar o chamado ao usuário
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE,  null=True, blank=True)
    responsavel = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, related_name='chamados_responsavel')



    def __str__(self):
        return f'{self.codigo}, {self.tipo}, {self.categoria}, {self.titulo}, {self.descricao}, {self.prioridade},{self.usuario}'
