DOCKER_REPO=index.docker.io
IMAGE_NAME=eufast/fast-webapp
IMAGE_TAG=0.1.0
K8S_NAMESPACE=fast-platform
K8S_POD_LABEL=platform\=fast,module\=core,app\=webapp
K8S_POD_CONTAINER=webapp
SHELL?=/bin/bash

# HELP
# This will output the help for each task
# thanks to https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
.PHONY: help

help: ## This help.
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.DEFAULT_GOAL := help

# COMPOSE TASKS

compose-build:
	docker-compose build

compose-start:
	docker-compose up

compose-stop:
	docker-compose down

compose-bash:
	docker exec -ti webapp bash

# DOCKER TASKS
# Build the container
build: ## Build the container
	docker build -t $(IMAGE_NAME) .

# Docker publish
publish: tag ## Publish the taged container
	docker push $(DOCKER_REPO)/$(IMAGE_NAME):$(IMAGE_TAG)

# Docker tagging
tag: ## Generate container tag
	docker tag $(IMAGE_NAME) $(DOCKER_REPO)/$(IMAGE_NAME):$(IMAGE_TAG)

list: ## List pods
	kubectl -n $(K8S_NAMESPACE) get pod -l $(K8S_POD_LABEL)

describe: ## Describe pods
	kubectl -n $(K8S_NAMESPACE) describe pod -l $(K8S_POD_LABEL)

ssh: ## SSH into the container
	kubectl -n $(K8S_NAMESPACE) exec -ti -c $(K8S_POD_CONTAINER) $$(kubectl -n $(K8S_NAMESPACE) get pod -l $(K8S_POD_LABEL) -o jsonpath="{.items[0].metadata.name}") $(SHELL)

log: ## Tail logs (stdout) of the container
	kubectl -n $(K8S_NAMESPACE) logs $$(kubectl -n $(K8S_NAMESPACE) get pod -l $(K8S_POD_LABEL) -o jsonpath="{.items[0].metadata.name}") $(K8S_POD_CONTAINER) -f

redeploy: ## Kill and redeploy the running container
	kubectl -n $(K8S_NAMESPACE) delete $$(kubectl -n $(K8S_NAMESPACE) get pod -l $(K8S_POD_LABEL) -o name)
