# Generated by Django 3.2.8 on 2021-10-20 07:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("posts", "0005_upvote"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="post",
            name="upvote",
        ),
        migrations.AlterField(
            model_name="upvote",
            name="post",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="upvote",
                to="posts.post",
            ),
        ),
    ]