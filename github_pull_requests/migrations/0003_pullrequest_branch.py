# Generated by Django 5.1.7 on 2025-03-23 15:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('github_branches', '0002_alter_branch_repo'),
        ('github_pull_requests', '0002_pullrequest_body'),
    ]

    operations = [
        migrations.AddField(
            model_name='pullrequest',
            name='branch',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pull_request_branch', to='github_branches.branch'),
        ),
    ]
