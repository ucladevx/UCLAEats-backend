default: build run

build: 
	docker-compose build

run:
	docker-compose up 

stop:
	docker-compose down

clean:
	docker-compose rm postgres
	docker-compose rm web
