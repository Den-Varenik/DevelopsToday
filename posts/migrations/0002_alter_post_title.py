# Generated by Django 3.2.8 on 2021-10-19 11:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("posts", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="title",
            field=models.CharField(max_length=100, verbose_name="Title"),
        ),
    ]
