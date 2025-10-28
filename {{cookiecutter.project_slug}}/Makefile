.PHONY: help install run test docker-build docker-up k8s-deploy clean

help:  ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install:  ## Install dependencies
	python3 -m pip install -r requirements.txt
	python3 -m pip install -r requirements-dev.txt

run:  ## Run the application locally
{% if cookiecutter.web_framework == 'fastapi' %}
	python3 -m src.app_fastapi
{% else %}
	python3 -m src.app_flask
{% endif %}

test:  ## Run tests
	python3 -m pytest src/tests/ -v --cov=src

docker-build:  ## Build Docker image
	docker build -t {{ cookiecutter.docker_registry }}/{{ cookiecutter.project_slug }}:latest .

docker-up:  ## Start with docker compose
	docker compose up -d

docker-down:  ## Stop docker compose
	docker compose down

k8s-deploy:  ## Deploy to Kubernetes
	kubectl apply -f k8s/ -n {{ cookiecutter.kubernetes_namespace }}

k8s-delete:  ## Delete from Kubernetes
	kubectl delete -f k8s/ -n {{ cookiecutter.kubernetes_namespace }}

helm-deploy:  ## Deploy with Helm
	helm upgrade --install {{ cookiecutter.project_slug }} ./helm/{{ cookiecutter.project_slug }} \
		--namespace {{ cookiecutter.kubernetes_namespace }} \
		--create-namespace

helm-delete:  ## Delete Helm release
	helm uninstall {{ cookiecutter.project_slug }} -n {{ cookiecutter.kubernetes_namespace }}

clean:  ## Clean up
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name '*.pyc' -delete
	find . -type f -name '*.pyo' -delete
	rm -rf .pytest_cache .coverage htmlcov/
