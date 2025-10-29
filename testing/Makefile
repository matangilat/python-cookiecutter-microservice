.PHONY: help install run test docker-build docker-up k8s-deploy clean

help:  ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install:  ## Install dependencies
	python3 -m pip install -r requirements.txt
	python3 -m pip install -r requirements-dev.txt

run:  ## Run the application locally

	python3 -m src.app_flask


test:  ## Run tests
	python3 -m pytest src/tests/ -v --cov=src

docker-build:  ## Build Docker image
	docker build -t ghcr.io/yourorg/testing:latest .

docker-up:  ## Start with docker compose
	docker compose up -d

docker-down:  ## Stop docker compose
	docker compose down

k8s-deploy:  ## Deploy to Kubernetes
	kubectl apply -f k8s/ -n default

k8s-delete:  ## Delete from Kubernetes
	kubectl delete -f k8s/ -n default

helm-deploy:  ## Deploy with Helm
	helm upgrade --install testing ./helm/testing \
		--namespace default \
		--create-namespace

helm-delete:  ## Delete Helm release
	helm uninstall testing -n default

clean:  ## Clean up
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name '*.pyc' -delete
	find . -type f -name '*.pyo' -delete
	rm -rf .pytest_cache .coverage htmlcov/
