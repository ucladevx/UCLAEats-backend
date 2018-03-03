# Dev commands
default: build-dev run-dev

build-dev:
	docker-compose -f docker-compose.dev.yml build

run-dev:
	docker-compose -f docker-compose.dev.yml up


# Prod commands
prod: prod-build prod-up

prod-build: 
	docker-compose build 

prod-up:
	docker-compose up -d

prod-down:
	docker-compose stop

clean:
	docker-compose rm postgres
	docker-compose rm web
