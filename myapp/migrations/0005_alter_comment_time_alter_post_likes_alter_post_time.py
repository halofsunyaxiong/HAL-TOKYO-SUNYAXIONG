# Generated by Django 4.1.7 on 2023-04-22 12:16

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("myapp", "0004_userinfo_address_userinfo_dob_alter_comment_time_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="comment",
            name="time",
            field=models.DateTimeField(
                blank=True, default=datetime.datetime(2023, 4, 22, 17, 46, 13, 961428)
            ),
        ),
        migrations.AlterField(
            model_name="post",
            name="likes",
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name="post",
            name="time",
            field=models.DateTimeField(
                blank=True, default=datetime.datetime(2023, 4, 22, 17, 46, 13, 961428)
            ),
        ),
    ]
