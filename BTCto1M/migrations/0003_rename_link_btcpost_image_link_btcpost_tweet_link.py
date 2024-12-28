# Generated by Django 4.2.7 on 2024-12-27 22:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("BTCto1M", "0002_alter_btcpost_btc_price"),
    ]

    operations = [
        migrations.RenameField(
            model_name="btcpost",
            old_name="link",
            new_name="image_link",
        ),
        migrations.AddField(
            model_name="btcpost",
            name="tweet_link",
            field=models.URLField(default=None, max_length=100),
            preserve_default=False,
        ),
    ]