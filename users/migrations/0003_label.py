# Generated by Django 2.2 on 2019-05-22 09:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20190505_1749'),
    ]

    operations = [
        migrations.CreateModel(
            name='Label',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('labelfor', models.SmallIntegerField()),
                ('content', models.CharField(max_length=12)),
            ],
        ),
    ]
