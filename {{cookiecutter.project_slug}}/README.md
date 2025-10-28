# {{ cookiecutter.project_name }}

{{ cookiecutter.project_description }}

## 🏗️ Architecture

- **Framework**: {{ cookiecutter.web_framework }}
- **Database**: {{ cookiecutter.database_type }}{% if cookiecutter.deploy_database == 'yes' %} (deployed with service){% endif %}
- **Queue**: {{ cookiecutter.queue_type }}{% if cookiecutter.deploy_queue == 'yes' %} (deployed with service){% endif %}
- **Cache**: {{ cookiecutter.cache_type }}{% if cookiecutter.deploy_cache == 'yes' %} (deployed with service){% endif %}
- **Monitoring**: {% if cookiecutter.enable_metrics == 'yes' %}Prometheus{% endif %}{% if cookiecutter.enable_node_exporter == 'yes' %} + Node Exporter{% endif %}

## 🚀 Quick Start

### Local Development

```bash
# On Debian/Ubuntu, install venv first (one-time setup)
sudo apt-get update
sudo apt-get install -y python3-venv python3-pip

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
python3 -m pip install -r requirements.txt

# Run API
python3 -m src.main

{% if cookiecutter.use_async_workers == 'yes' %}# Run Worker (in another terminal)
python3 -m src.worker
{% endif %}
```

### Docker Compose (Full Stack)

```bash
# Start all services
docker compose up

# API: http://localhost:8000
{% if cookiecutter.deploy_monitoring_stack == 'yes' %}# Grafana: http://localhost:3000
# Prometheus: http://localhost:9090
{% endif %}
```

### Kubernetes Deployment

```bash
# Deploy everything (including infrastructure)
kubectl apply -f k8s/ -n {{ cookiecutter.kubernetes_namespace }}

# Or use Helm
helm install {{ cookiecutter.project_slug }} ./helm/{{ cookiecutter.project_slug }} \
  --namespace {{ cookiecutter.kubernetes_namespace }} \
  --create-namespace
```

## 📁 Project Structure

```
{{ cookiecutter.project_slug }}/
├── src/
│   ├── api/              # API endpoints and routes
│   ├── classes/          # Business logic and domain models
│   │   ├── models/       # Data models (entities & schemas)
│   │   ├── services/     # Business logic layer
│   │   └── repositories/ # Data access layer
│   ├── utils/            # Utilities and infrastructure
│   └── tests/            # All tests (unit & integration)
├── k8s/
│   ├── infrastructure/   # Optional infrastructure deployments
│   └── monitoring/       # Monitoring stack
└── helm/                 # Helm charts
```

## 🔧 Configuration

Edit `config/infrastructure.yaml` to customize your setup.

## 📊 Monitoring

{% if cookiecutter.enable_metrics == 'yes' %}- **Metrics**: http://localhost:8000/metrics
{% endif %}{% if cookiecutter.enable_node_exporter == 'yes' %}- **Node Metrics**: http://localhost:9100/metrics
{% endif %}{% if cookiecutter.deploy_monitoring_stack == 'yes' %}- **Prometheus**: http://localhost:9090
- **Grafana**: http://localhost:3000 (admin/admin)
{% endif %}
## 📚 Documentation

- [Deployment Guide](docs/DEPLOYMENT.md)
- [Development Guide](docs/DEVELOPMENT.md)
- [API Documentation](http://localhost:8000/docs) (when running)

## 👤 Author

{{ cookiecutter.author_name }} <{{ cookiecutter.author_email }}>

## 📄 License

MIT
