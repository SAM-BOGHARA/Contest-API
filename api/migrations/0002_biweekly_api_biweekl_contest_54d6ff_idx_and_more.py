# Generated by Django 4.2.4 on 2023-08-18 17:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='biweekly',
            index=models.Index(fields=['contest_id', 'page'], name='api_biweekl_contest_54d6ff_idx'),
        ),
        migrations.AddIndex(
            model_name='weekly',
            index=models.Index(fields=['contest_id', 'page'], name='api_weekly_contest_4d435a_idx'),
        ),
    ]
