# RentManager API

Phase 0 scaffold for the RentManager modular monolith migration.

## Run locally

1. Install dependencies:

   `pip install -e .[dev]`

2. Start the API:

   `uvicorn rentmanager.main:app --reload`

## Endpoints

- `GET /health`
- `POST /api/v1/auth/login`
- `GET /api/v1/auth/me`
