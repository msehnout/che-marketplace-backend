build-docker:
	docker build -t che_marketplace_backend .

run-docker: build-docker
	docker run -p 8080:8080 -e CHE_PLUGIN_DEV_TOKEN=${CHE_PLUGIN_DEV_TOKEN} che_marketplace_backend

run-local:
	bash run.sh
