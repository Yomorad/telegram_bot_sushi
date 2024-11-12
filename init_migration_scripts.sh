


echo "Applying migrations..."
alembic revision --autogenerate -m "init migration"
alembic upgrade head
echo "Migrations applied successfully."
