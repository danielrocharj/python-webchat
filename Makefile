.SILENT:

up-local:
	docker-compose -f docker-compose.yml up

up-local-force-recreate:
	docker-compose -f docker-compose.yml up --build --force-recreate

down-local:
	docker-compose -f docker-compose.yml down --remove-orphans

access:
	docker exec -it some-webchat /bin/bash
