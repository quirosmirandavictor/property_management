# RentManager API

Phase 0 scaffold for the RentManager modular monolith migration.

## Run locally

1. Install dependencies:

   `pip install -e .[dev]`

2. Start the API:

   `uvicorn rentmanager.main:app --reload`

##  🐳  Run with Docker

1. Build and start the API with Docker Compose:

   `docker-compose up`

2. The API will be available at `http://localhost:8000`

3. To stop the services:

   `docker-compose down`

4. To rebuild the image after code changes:

   `docker-compose up --build`

## Environment Configuration

Create a `.env` file in the `rentmanager-api` directory with the following variables:

```env
APP_NAME=RentManager API
APP_ENV=dev
APP_DEBUG=true
DATABASE_URL=mysql+pymysql://rentmanager:rentmanager@localhost:3306/rentmanager
```

## Endpoints

- `GET /health`
- `POST /api/v1/auth/login`
- `GET /api/v1/auth/me`
