# Alembic Migrations for ContentFlow AI

- Use `alembic revision --autogenerate -m "message"` to create a new migration.
- Use `alembic upgrade head` to apply migrations.
- Make sure the `CFLOW_DB_URL` environment variable is set to your Neon PostgreSQL or local DB URL.
- Migrations use models from `src/api/models/core.py`.
