# Generated by Django 2.2 on 2019-05-07 03:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0002_auto_20190505_1749'),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('country', models.CharField(default='中国', max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Press',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('cover', models.ImageField(upload_to='')),
                ('intro', models.CharField(max_length=100)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='anthor_book', to='book.Author')),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='city_book', to='users.City')),
                ('press', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='press_book', to='book.Press')),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='school_book', to='users.School')),
            ],
        ),
    ]