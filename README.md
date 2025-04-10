# fastapi-lite-boilerplate
## Lightweight boilerplate for FastAPI application


## Docker

`docker build -t fastapi-boilerplate:{version specified in compose.yaml} .` - builds an image

`cp .env.example .env` - make a copy of .env file

Replace default environment variables (postgres user, password etc.)

`docker compose -f compose.yaml -p up` - runs containers 


## Database

### Migrations

`alembic revision --autogenerate` - creates migration script (alembic/versions) 

`alembic upgrade head` - makes migration according to last version of database
