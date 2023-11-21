help:
	@echo ''
	@echo 'Usage: make [TARGET]'
	@echo 'Targets:'
	@echo '  build    	build docker images'
	@echo '  start    	Start url shortener  service'
	@echo '  stop     	Stop url shortener  service'
	@echo '  test     	test url shortener  service'
	@echo '  help     	this text'

build:
	docker compose build

start:
	@echo "Starting url shortener service..."
	docker compose up --build -d
	@echo "Done"

stop:
	docker compose down

test:
	docker compose exec flask-app python test.py