# Generated by Django 4.2.2 on 2023-07-04 02:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('price', '0002_alter_dailyusage_table'),
    ]

    operations = [
        migrations.CreateModel(
            name='MonthlyUsage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.CharField(max_length=10)),
                ('price', models.IntegerField()),
            ],
            options={
                'db_table': 'monthly_usage',
            },
        ),
    ]