# Dev commands
default: dev-build dev-run

dev-build:
	docker-compose -f ./docker-compose.dev.yml build

dev-run:
	docker-compose -f ./docker-compose.dev.yml up


# Prod commands
prod: prod-build prod-up

prod-build: 
	docker-compose -f ./docker-compose.yml build 

prod-up:
	docker-compose -f ./docker-compose.yml up -d

prod-down:
	docker-compose -f ./docker-compose.yml stop

clean:
	docker-compose -f ./docker-compose.yml rm postgres
	docker-compose -f ./docker-compose.yml rm api

secrets:
	tar -cvzf BruinBiteSecrets.tar.gz *.pem *.env *.p12

unlock:
	git-crypt unlock ./BruinBiteSecretKey.key
	tar -xvzf BruinBiteSecrets.tar.gz
