# Generated by Django 5.1.7 on 2025-03-21 08:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('github_pull_requests', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pullrequest',
            name='title',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
