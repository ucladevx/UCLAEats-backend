# Dev commands
default: build-dev run-dev

build-dev:
	docker-compose -f ./docker-compose.dev.yml build

run-dev:
	docker-compose -f ./docker-compose.dev.yml up


# Prod commands
prod: prod-build prod-up

prod-build: 
	docker-compose build 

prod-up:
	docker-compose -f ./docker-compose.yml up -d

prod-down:
	docker-compose -f ./docker-compose.yml stop

clean:
	docker-compose -f ./docker-compose.yml rm postgres
	docker-compose -f ./docker-compose.yml rm api
