# Generated by Django 3.2.2 on 2021-05-21 07:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('demos', '0009_alter_sample_exp'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='sample',
            index=models.Index(fields=['exp'], name='demos_sampl_exp_a00fca_idx'),
        ),
    ]
