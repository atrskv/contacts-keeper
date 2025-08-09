dev-up:
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml --env-file .env.dev up -d --build

prod-up:
	docker-compose -f docker-compose.yml -f docker-compose.prod.yml --env-file .env.prod up -d --build

dev-down:
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml down

prod-down:
	docker-compose -f docker-compose.yml -f docker-compose.prod.yml down
