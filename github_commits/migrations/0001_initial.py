# Generated by Django 5.1.7 on 2025-03-25 09:07

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('github_branches', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Commit',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('message', models.CharField(blank=True, max_length=255, null=True)),
                ('pushed_at', models.DateTimeField()),
                ('modified_files', models.JSONField()),
                ('author_name', models.CharField(max_length=255)),
                ('author_email', models.CharField(max_length=255)),
                ('author_username', models.CharField(max_length=255)),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='commits', to='github_branches.branch')),
            ],
        ),
    ]
