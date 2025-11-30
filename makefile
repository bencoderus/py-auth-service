# Local development
start:
	uv run uvicorn src.main:app --reload

# Docker commands
docker-build:
	docker-compose build

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

docker-restart:
	docker-compose restart

docker-logs:
	docker-compose logs -f

docker-logs-web:
	docker-compose logs -f web

docker-ps:
	docker-compose ps

docker-clean:
	docker-compose down -v

docker-rebuild:
	docker-compose up -d --build

# Database migrations in Docker (migrations run automatically on startup)
docker-migrate:
	@echo "Note: Migrations run automatically on container startup"
	docker-compose exec web alembic upgrade head

docker-migrate-rollback:
	docker-compose exec web alembic downgrade -1

# Access services
docker-db-shell:
	docker-compose exec postgres psql -U postgres -d auth_db

docker-redis-cli:
	docker-compose exec redis redis-cli -a redis_password

docker-web-shell:
	docker-compose exec web /bin/bash