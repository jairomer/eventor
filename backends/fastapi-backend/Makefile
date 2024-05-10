test:
	pytest .

generate-api-key:
	./setenvkey.sh

run:
	uvicorn main:app --app-dir ./app

run-reload:
	uvicorn main:app --app-dir ./app --reload

up:
	poetry export -f requirements.txt --without-hashes > requirements.txt
	docker compose up --build

build:
	poetry export -f requirements.txt --without-hashes > requirements.txt
	docker build . -t eventor-api
