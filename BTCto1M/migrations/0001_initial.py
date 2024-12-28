# Generated by Django 4.2.7 on 2024-12-27 21:45

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="BTCPost",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("btc_price", models.IntegerField(max_length=8)),
                ("post_time", models.DateTimeField(auto_now_add=True)),
                ("link", models.URLField(max_length=100)),
            ],
        ),
    ]
