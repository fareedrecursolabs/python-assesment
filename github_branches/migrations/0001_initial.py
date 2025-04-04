# Generated by Django 5.1.7 on 2025-03-25 09:07

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('github_repos', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Branch',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('repo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='branches', to='github_repos.githubrepo')),
            ],
        ),
    ]
