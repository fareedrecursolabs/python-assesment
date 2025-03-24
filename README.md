# Repository Explorer Backend

A Django-based backend that integrates with GitHub webhooks to capture repository events such as commits, pull requests (PRs), and merges. The backend stores this data in a PostgreSQL database and provides real-time commit updates using Server-Sent Events (SSE) with Redis.

## Features

- **GitHub Webhook Integration**: Automatically captures push, PR, and merge events.
- **PostgreSQL Database**: Stores repository, commit, and pull request data efficiently.
- **Server-Sent Events (SSE)**: Provides real-time commit updates to connected clients.
- **Redis for Pub/Sub**: Manages real-time updates and event streaming.
- **Django Rest Framework (DRF)**: Provides API endpoints for repository data access.
- **CORS Support**: Allows cross-origin requests for frontend integration.

## Technologies Used

- **Django**: Python web framework
- **Django Rest Framework (DRF)**: API development
- **PostgreSQL**: Relational database
- **Redis**: Real-time event broadcasting
- **Daphne & Channels**: WebSocket and SSE support
- **Server-Sent Events (SSE)**: Live commit updates
- **GitHub Webhooks**: Automatic data ingestion
- **CORS Headers**: Cross-origin support

## Installation

### Prerequisites

- Python 3.10+
- PostgreSQL
- Redis
- GitHub account for webhook setup

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/repository-explorer-backend.git
   cd repository-explorer-backend
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   Create a `.env` file and add:
   ```ini
   SECRET_KEY=your_secret_key
   DATABASE_NAME=your_db_name
   DATABASE_USER=your_db_user
   DATABASE_PASSWORD=your_db_password
   DATABASE_HOST=localhost
   DATABASE_PORT=5432
   REDIS_URL=redis://localhost:6379/0
   GITHUB_WEBHOOK_SECRET=your_webhook_secret
   ```

5. **Apply migrations and create superuser**
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

6. **Run the Redis server** (Ensure Redis is installed)
   ```bash
   redis-server
   ```

7. **Run the Django development server**
   ```bash
   python manage.py runserver
   ```

## Webhook Setup

1. Go to your GitHub repository settings.
2. Navigate to **Webhooks** > **Add webhook**.
3. Set the payload URL to your backend endpoint (e.g., `http://backendURL.com/github/`).
4. Select `application/json` as the content type.
5. Enter the **secret** key (same as in `.env`).
6. Choose webhook events (push, pull request, merge, etc.).
7. Save and test the webhook.

## API Endpoints

| Method | Endpoint                     | Description                   |
|--------|------------------------------|-------------------------------|
| GET    | `repos/`                | List all repositories              |
| GET    | `repos/{id}/`           | Retrieve a repository              |
| GET    | `commits/{branch_id}/`              | List all commits       |
| GET    | `commits/{branch_id}/{id}/`         | Retrieve a specific commit    |
| GET    | `pull_requests/{repo_id}/`        | List pull requests       |
| GET    | `pull_requests/{repo_id}/{id}/`   | Retrieve a specific PR    |
| GET    | `branch/{repo_id}`        | List braches                     |
| GET    | `branch/{repo_id}/{id}/`   | Retrieve a specific branch       |
| GET    | `real_time_update/stream/commit/{branch_id}`       | Subscribe to real-time events |

```

## Deployment

1. **Setup PostgreSQL and Redis on the server.**
2. **Use Gunicorn and Daphne for production.**
   ```bash
   gunicorn backend.wsgi:application --bind 0.0.0.0:8000 --workers 4
   ```
3. **Use Nginx as a reverse proxy.**
4. **Set up SSL using Let's Encrypt.**
