# Generated by Django 4.1.7 on 2023-04-02 08:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Revaluation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Application_type', models.CharField(max_length=100)),
                ('Hallticket', models.CharField(max_length=20)),
                ('Student_Name', models.CharField(max_length=250)),
                ('Subject_code', models.CharField(max_length=50)),
                ('Subject', models.CharField(max_length=200)),
                ('Mobile', models.CharField(max_length=10)),
                ('Dhondi_id', models.IntegerField()),
                ('Amount', models.IntegerField()),
            ],
        ),
    ]