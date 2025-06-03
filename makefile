.PHONY: up down build test clean
COMPOSE_FILE := ./dev/docker-compose.yml
TEST_COMPOSE_FILE := ./tests/docker-compose.test.yml

build:
	docker compose -f $(COMPOSE_FILE) build

up:
	docker compose -f $(COMPOSE_FILE) up -d

down:
	docker compose -f $(COMPOSE_FILE) down

test:
	docker compose -f $(TEST_COMPOSE_FILE) up --build --abort-on-container-exit tests

clean:
	docker compose -f $(COMPOSE_FILE) down -v --remove-orphans
	docker compose -f $(TEST_COMPOSE_FILE) down -v --remove-orphans
