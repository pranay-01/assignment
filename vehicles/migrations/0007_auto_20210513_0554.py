# Generated by Django 3.2.2 on 2021-05-13 05:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vehicles', '0006_auto_20210512_1243'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bike',
            options={'ordering': ('id',)},
        ),
        migrations.AlterModelOptions(
            name='car',
            options={'ordering': ('id',)},
        ),
        migrations.AlterModelOptions(
            name='custom',
            options={'ordering': ('id',)},
        ),
        migrations.AlterModelOptions(
            name='displayplace',
            options={'ordering': ('id',)},
        ),
        migrations.AlterModelOptions(
            name='manufacturer',
            options={'ordering': ('id',)},
        ),
    ]
