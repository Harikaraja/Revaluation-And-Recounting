# Generated by Django 4.1.7 on 2023-04-08 10:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rev', '0002_regulations_with_grades'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subject_max_marks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Brach_code', models.CharField(max_length=20)),
                ('Max_marks', models.IntegerField()),
                ('Max_Total_marks', models.IntegerField()),
                ('Min_marks', models.IntegerField()),
                ('Min_Total_marks', models.IntegerField()),
                ('Credit', models.IntegerField()),
                ('Subject_type', models.IntegerField()),
                ('Subject_codes', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='Subject_codes', to='rev.revaluation')),
                ('Subjects', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='Subjects', to='rev.revaluation')),
            ],
        ),
        migrations.DeleteModel(
            name='Regulations_19',
        ),
        migrations.DeleteModel(
            name='Regulations_20',
        ),
    ]