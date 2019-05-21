# Generated by Django 2.2 on 2019-05-16 08:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0002_auto_20190505_1749'),
    ]

    operations = [
        migrations.CreateModel(
            name='FriendShip',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fa', models.CharField(max_length=10)),
                ('fb', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='FriendRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=10)),
                ('request_time', models.DateTimeField(auto_now=True)),
                ('deal_time', models.DateTimeField()),
                ('message', models.CharField(max_length=50)),
                ('propser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reader_friendrequest', to='users.Reader')),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reader_friendreceive', to='users.Reader')),
            ],
        ),
    ]