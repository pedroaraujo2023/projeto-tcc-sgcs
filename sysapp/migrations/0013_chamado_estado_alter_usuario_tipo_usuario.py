# Generated by Django 4.2.7 on 2023-12-08 02:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sysapp', '0012_remove_chamado_id_alter_chamado_codigo'),
    ]

    operations = [
        migrations.AddField(
            model_name='chamado',
            name='estado',
            field=models.CharField(choices=[('Novos', 'Novos'), ('Em andamento', 'Em andamento'), ('Finalizados', 'Finalizados')], default='Novos', max_length=20, verbose_name='Estado'),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='tipo_usuario',
            field=models.CharField(choices=[('Servidor', 'Servidor'), ('Aluno', 'Aluno')], default='1', max_length=8, verbose_name='Tipo de Usuário'),
        ),
    ]