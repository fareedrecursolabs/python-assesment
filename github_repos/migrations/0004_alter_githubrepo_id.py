# Generated by Django 5.1.7 on 2025-03-20 14:03

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('github_repos', '0003_alter_githubrepo_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='githubrepo',
            name='id',
            field=models.IntegerField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]
