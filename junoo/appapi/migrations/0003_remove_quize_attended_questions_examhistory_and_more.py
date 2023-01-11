# Generated by Django 4.1.4 on 2022-12-07 18:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quizes', '0001_initial'),
        ('questions', '0001_initial'),
        ('appapi', '0002_remove_quize_attended_questions_quize_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='quize_attended_questions',
            name='ExamHistory',
        ),
        migrations.RemoveField(
            model_name='quize_attended_questions',
            name='ExamList',
        ),
        migrations.AddField(
            model_name='quize_attended_questions',
            name='quize',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='quizes.quize'),
        ),
        migrations.AddField(
            model_name='quize_attended_questions',
            name='quizehistory',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='appapi.quizehistory'),
        ),
        migrations.CreateModel(
            name='Exam_attended_questions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quize_attended_code', models.CharField(blank=True, max_length=200, null=True)),
                ('right_wrong', models.BooleanField(blank=True, default=False, null=True)),
                ('crt_option', models.CharField(blank=True, max_length=200, null=True)),
                ('ExamHistory', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='appapi.examhistory')),
                ('ExamList', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='quizes.examlist')),
                ('customer', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='appapi.customer')),
                ('question', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='questions.questions')),
            ],
        ),
    ]
