## Tools
### Docker
Our project uses Docker for development and deployment.  You should [download
Docker](https://store.docker.com/search?type=edition&offering=community)
(community edition), then run through the [Docker
Tutorial](https://docs.docker.com/get-started/) to familiarize yourself with Docker commands and how they work. The Makefile depends on Docker.

### Git-Crypt
git-crypt: We use git-crypt to decrypt files environment files and keys usage automatically while pushing/pulling.
On Mac, install git-crypt using `brew install git-crypt`. Otherwise follow the INSTALL.md in the [git-crypt repo.](https://github.com/AGWA/git-crypt)
To use git-crypt, one must have the BruinBiteSecretKey.key file, which will be
distributed to each developer through other means.  `make secrets` and `make unlock` rely on this tool.

## Installation Instructions
Using this repo requires Docker, docker-compose, and git-crypt. See the above sections on how to install them.
After installing them, to set up the repo would require:

1. Start Docker
2. Download the BruinBitSecretKey.key into the repo
3. Run `make unlock` to use the key to unlock the secrets
4. Then run `make` (this step may take a while, you can use the -j flag to speed this up)

# Makefile

## Make commands for dev
- make unlock: Decrypts files and untars secrets. Will move files that might be overwritten into a directory based on the git branch name (e.g. master-secrets/)
- make: by default will build the development containers defined in
  docker-compose.dev.yml, and then calls docker-compose up on those containers
- make dev-build: Builds containers defined in docker-compose.dev.yml
- make dev-run:  Calls docker-compose up on containers.
Use Crtl-C to stop the containers
- make dev-down: This deletes all the cached containers and volumes. This is especially critical for Postgres containers which will otherwise be reused despite being stopped, restarted, or even survive having the container removed.
- make clean: Removes all generated files
- make secrets: Makes tar file of env/pem files

## Make commands for production
Instructions for running/deploying stuff on production servers. You should not normally do this on your own computer.
- make prod: builds and runs containers in detached mode
- prod-build: builds containers in docker-compose.yml
- prod-up: calls docker-compose up in detached mode on containers
  (docker-compose.yml)
- prod-down: Stops containers defined in docker-compose.yml

### INSTALLING DOCKER AND DOCKER-COMPOSE ON REMOTE
- sudo yum update -y # update
- sudo yum install docker -y # install docker
- sudo service docker start # start docker as a service in the background
- sudo usermod a -G ec2-user # add ec2-user to docker group, to use docker w/o sudo.
- sudo curl -L
  https://github.com/docker/compose/releases/download/1.19.0/docker-compose-`uname
  -s`-`uname -m` -o /usr/local/bin/docker-compose
- sudo chmod +x /usr/local/bin/docker-compose

## General Debugging Tips:
- To listen to logs from python run `docker logs -f <CONTAINER_ID>`. You can find the container ID by running `docker ps`.