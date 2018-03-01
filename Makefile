default: build run

build: 
	docker-compose build web

run:
	docker-compose up 

stop:
	docker-compose down

run-prod:
	docker-compose up -d

clean:
	docker-compose rm postgres
	docker-compose rm web
