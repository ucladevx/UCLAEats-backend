# Dev commands
default: dev-build dev-run

dev-build:
	docker-compose -f ./docker-compose.dev.yml build

dev-run:
	docker-compose -f ./docker-compose.dev.yml up

dev-down: # deletes all the docker local cached containers/volumes
	docker-compose -f ./docker-compose.dev.yml down


# Prod commands
prod: prod-build prod-up

prod-build: 
	docker-compose -f ./docker-compose.yml build 

prod-up:
	docker-compose -f ./docker-compose.yml up -d

prod-stop:
	docker-compose -f ./docker-compose.yml stop

clean:
	docker-compose -f ./docker-compose.yml rm postgres
	docker-compose -f ./docker-compose.yml rm api

secrets:
	tar -cvzf BruinBiteSecrets.tar.gz *.pem *.env 

unlock:
	-git-crypt unlock ./BruinBiteSecretKey.key
	-name="$$(git rev-parse --abbrev-ref HEAD)-secrets/";\
	mkdir $$name; \
	mv *.env $$name; \
	mv *.pem $$name
	tar -xvzf BruinBiteSecrets.tar.gz
