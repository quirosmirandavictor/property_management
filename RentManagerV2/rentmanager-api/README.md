# RentManager API

Phase 0 scaffold for the RentManager modular monolith migration.

## Getting Started

### Prerequisites

Make sure the following tools are available before running the project:

- Python 3.12+
- Docker Desktop 4+
- Docker Compose v2 (`docker compose`)
- Git

### Verify local tools

Run these commands to confirm your environment:

```bash
python --version
docker --version
docker compose version
git --version
```

If one tool is missing, install it first:

- Python: https://www.python.org/downloads/
- Docker Desktop: https://www.docker.com/products/docker-desktop/
- Git: https://git-scm.com/downloads

### Repository bootstrap

1. Clone the repository and move into the API folder.
2. Create your environment file:

   `cp .env.example .env`

3. If your shell does not support `cp` (for example, PowerShell), use:

   `Copy-Item .env.example .env`

4. Keep Docker Desktop running before starting services.

### First run recommendation

Use Docker first to avoid local dependency drift:

1. `docker compose up --build`
2. Confirm health check:

   `curl http://localhost:8000/health`

3. Stop services when done:

   `docker compose down`

If Docker is not available yet, use the local Python flow in the next section.

## Run locally

1. Copy the environment template:

   `cp .env.example .env`

2. Install dependencies:

   `pip install -e .[dev]`

3. Apply database migrations:

   `alembic upgrade head`

4. Start the API:

   `uvicorn rentmanager.main:app --reload`

## 🐳 Run with Docker (API + MySQL)

1. Copy the environment template:

   `cp .env.example .env`

2. Build and start API + MySQL:

   `docker compose up --build`

3. The API will be available at `http://localhost:8000`

4. Run tests inside containers:

   `docker compose --profile test run --rm tests`

5. To stop the services:

   `docker compose down`

6. To stop services and remove MySQL data volume:

   `docker compose down -v`

## Environment Configuration

Create a `.env` file in the `rentmanager-api` directory with the following variables:

```env
APP_NAME=RentManager API
APP_ENV=dev
APP_DEBUG=true
APP_SECRET_KEY=change-me-in-real-environments-32b
JWT_ALGORITHM=RS256
JWT_PRIVATE_KEY_PATH=.keys/private_key.pem
JWT_PUBLIC_KEY_PATH=.keys/public_key.pem
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7
DATABASE_URL=mysql+pymysql://rentmanager:rentmanager@mysql:3306/rentmanager
```

Notes:

- Inside Docker Compose, use `mysql` as database host.
- Outside Docker, use `localhost` if your MySQL server runs on the local machine.
- For development and tests, if RSA key files are not present, the app can use ephemeral keys.

## Endpoints

- `GET /health`
- `POST /api/v1/auth/login`
- `POST /api/v1/auth/refresh`
- `POST /api/v1/auth/logout`
- `GET /api/v1/auth/me`
