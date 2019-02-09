# Generated by Django 2.1.5 on 2019-02-06 18:45

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('toDo', '0004_auto_20190204_1823'),
    ]

    operations = [
        migrations.AlterField(
            model_name='singletask',
            name='list',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='toDo.ToDoList'),
        ),
        migrations.AlterField(
            model_name='todolist',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2019, 2, 6, 18, 45, 21, 326436)),
        ),
        migrations.AlterField(
            model_name='todolist',
            name='owner',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='toDo.User'),
        ),
    ]
