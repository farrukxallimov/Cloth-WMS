# Generated by Django 4.2.7 on 2025-05-26 11:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0003_alter_product_size'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='size',
            field=models.CharField(choices=[('XS', 'XS'), ('S', 'S'), ('M', 'M'), ('L', 'L'), ('XL', 'XL'), ('XXL', 'XXL'), ('3/4', '3/4'), ('5/6', '5/6'), ('7/8', '7/8'), ('9/10', '9/10'), ('11/12', '11/12'), ('13/14', '13/14'), ('2/10', '2/10'), ('2/20', '2/20')], max_length=10, verbose_name='O‘lcham'),
        ),
    ]
