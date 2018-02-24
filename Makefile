default: build run

build-image: 
	docker build -t terrenceho/dea-backend:latest .
	docker push terrenceho/dea-backend:latest

build: build-image
	docker-compose build

run:
	docker-compose up 

stop:
	docker-compose down

run-prod:
	docker-compose up -d

clean:
	docker-compose rm postgres
	docker-compose rm web
