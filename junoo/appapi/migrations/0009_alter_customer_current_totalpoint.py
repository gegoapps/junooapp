# Generated by Django 4.1.4 on 2022-12-17 17:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appapi', '0008_alter_customer_current_totalpoint'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='current_totalpoint',
            field=models.CharField(blank=True, default=0, max_length=200, null=True),
        ),
    ]
