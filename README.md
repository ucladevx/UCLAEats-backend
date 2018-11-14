# DEVELOPMENT
### Installation Instructions
Using this repo requires Docker, docker-compose, and git-crypt. See the following sections on how to install them.
After installing them, to set up the repo would require:

1. Start Docker
2. Download the BruinBitSecretKey.key into the repo
3. Run `make unlock` to use the key to unlock the secrets
4. Then run `make` (this step may take a while, you can use the -j flag to speed this up)

## Make commands for dev
- make unlock: Decrypts files and untars secrets
- make: by default will build the development containers defined in
  docker-compose.dev.yml, and then calls docker-compose up on those containers
- make dev-build: Builds containers defined in docker-compose.dev.yml
- make dev-run:  Calls docker-compose up on containers.
- make clean: Removes all generated files
- make secrets: Makes tar file of env/pem files

## Tools
### Docker
Our project uses Docker for development and deployment.  You should [download
Docker](https://store.docker.com/search?type=edition&offering=community)
(community edition), then run through the [Docker
Tutorial](https://docs.docker.com/get-started/) to familiarize yourself with Docker commands and how they work. The Makefile depends on Docker.

### Git-Crypt
git-crypt: We use git-crypt to decrypt files environment files and keys usage automatically while pushing/pulling.
On Mac, install git-crypt using `brew install git-crypt`. Otherwise follow the INSTALL.md in the [git-crypt repo.] (https://github.com/AGWA/git-crypt)
To use git-crypt, one must have the BruinBiteSecretKey.key file, which will be
distributed to each developer through other means.  `make secrets` and `make unlock` rely on this tool.

# PRODUCTION
Instructions for running/deploying stuff on production servers. You should not normally do this on your own computer.
## Make commands for production
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
