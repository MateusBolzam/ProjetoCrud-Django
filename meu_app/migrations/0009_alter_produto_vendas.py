# Generated by Django 5.0.6 on 2024-06-14 18:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meu_app', '0008_rename_compra_produto_estoque'),
    ]

    operations = [
        migrations.AlterField(
            model_name='produto',
            name='vendas',
            field=models.IntegerField(default=0),
        ),
    ]
