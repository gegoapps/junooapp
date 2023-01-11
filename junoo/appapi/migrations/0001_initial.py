# Generated by Django 4.1.4 on 2022-12-07 15:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('questions', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('quizes', '0001_initial'),
        ('masters', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True, null=True)),
                ('mobile', models.CharField(blank=True, max_length=200, null=True)),
                ('email', models.CharField(blank=True, max_length=200, null=True)),
                ('name', models.CharField(blank=True, max_length=200, null=True)),
                ('status', models.BooleanField(blank=True, default=False, null=True)),
                ('current_totalpoint', models.CharField(blank=True, default=0, max_length=200, null=True)),
                ('country_code', models.CharField(blank=True, max_length=200, null=True)),
                ('junoocategory', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='masters.junoocategory')),
                ('junoosubcategory', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='masters.junoosubcategory')),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='QuizeHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quize_attended_code', models.CharField(blank=True, max_length=200, null=True)),
                ('total_questions', models.CharField(blank=True, max_length=200, null=True)),
                ('total_right_answers', models.CharField(blank=True, max_length=200, null=True)),
                ('total_wrong_answer', models.CharField(blank=True, max_length=200, null=True)),
                ('customer', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='appapi.customer')),
                ('quize', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='quizes.quize')),
            ],
        ),
        migrations.CreateModel(
            name='Quize_attended_questions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quize_attended_code', models.CharField(blank=True, max_length=200, null=True)),
                ('right_wrong', models.BooleanField(blank=True, default=False, null=True)),
                ('crt_option', models.CharField(blank=True, max_length=200, null=True)),
                ('customer', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='appapi.customer')),
                ('question', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='questions.questions')),
                ('quize', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='quizes.quize')),
                ('quizehistory', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='appapi.quizehistory')),
            ],
        ),
        migrations.CreateModel(
            name='qanda_attended_log',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateField(auto_now_add=True, null=True)),
                ('right_answr', models.CharField(blank=True, max_length=200, null=True)),
                ('wrong_answr', models.CharField(blank=True, max_length=200, null=True)),
                ('skiped_answr', models.CharField(blank=True, max_length=200, null=True)),
                ('customer', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='appapi.customer')),
            ],
        ),
        migrations.CreateModel(
            name='PointHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateField(auto_now_add=True, null=True)),
                ('created_point', models.CharField(blank=True, max_length=200, null=True)),
                ('title', models.CharField(blank=True, max_length=200, null=True)),
                ('status', models.BooleanField(blank=True, default=False, null=True)),
                ('customer', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='appapi.customer')),
            ],
        ),
        migrations.CreateModel(
            name='CustomerFcm',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fcm_key', models.CharField(blank=True, max_length=200, null=True)),
                ('created_date', models.DateField(auto_now_add=True, null=True)),
                ('customer', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='appapi.customer')),
            ],
        ),
    ]
