# DEVELOPMENT
## Make commands
- make: by default will build the development containers defined in
  docker-compose.dev.yml, and then calls docker-compose up on those containers
- make dev-build: Builds containers defined in docker-compose.dev.yml
- make dev-run:  Calls docker-compose up on containers.
- make clean: Removes all generated files
- make secrets: Makes tar file of env/pem files
- make unlock: Decrypts files and untars secrets

## Tools
### Docker
Our project uses Docker for development and deployment.  You should [download
Docker](https://store.docker.com/search?type=edition&offering=community)
(community edition), then run through the [Docker
Tutorial](https://docs.docker.com/get-started/) to familiarize yourself with
Docker commands and how they work.  The Makefile depends on Docker.

### Git-Crypt
git-crypt: We use gitcrypt to decrypt files environment files and keys for
usage. To do this, one must have the BruinBiteSecretKey.key file, which will be
distributed to each developer through other means.  make secrets/unlock relies
on this tool.  You can install this tool through homebrew.

# PRODUCTION
## Make commands
- make prod: builds and runs containers in detached mode
- prod-build: builds containers in docker-compose.yml
- prod-up: calls docker-compose up in detached mode on containers
  (docker-compose.yml)
- prod-down: Stops containers definedin docker-compose.yml

## Installation Instructions
### INSTALLING DOCKER AND DOCKER-COMPOSE ON REMOTE
- sudo yum update -y # update
- sudo yum install docker -y # install docker
- sudo service docker start # start docker as a service in the background
- sudo usermod a -G ec2-user # add ec2-user to docker group, to use docker w/o sudo.
- sudo curl -L
  https://github.com/docker/compose/releases/download/1.19.0/docker-compose-`uname
  -s`-`uname -m` -o /usr/local/bin/docker-compose
- sudo chmod +x /usr/local/bin/docker-compose
