# Generated by Django 5.1.7 on 2025-03-25 09:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GithubRepo',
            fields=[
                ('id', models.BigIntegerField(editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('url', models.CharField(max_length=255)),
                ('owner_name', models.CharField(max_length=255)),
                ('owner_email', models.CharField(max_length=255)),
                ('main_branch', models.CharField(max_length=255)),
            ],
        ),
    ]
