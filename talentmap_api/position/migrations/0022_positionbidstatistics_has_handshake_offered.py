# Generated by Django 2.0.4 on 2019-03-04 16:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('position', '0021_auto_20181126_1814'),
    ]

    operations = [
        migrations.AddField(
            model_name='positionbidstatistics',
            name='has_handshake_offered',
            field=models.BooleanField(default=False),
        ),
    ]
