from django.apps import AppConfig


class GithubCommitsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'github_commits'

    def ready(self):
        import github_commits.signals
