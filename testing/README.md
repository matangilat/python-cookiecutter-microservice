# testing

A microservice built with the template

## 🏗️ Architecture

- **Framework**: flask
- **Database**: postgresql (deployed with service)
- **Queue**: kafka (deployed with service)
- **Cache**: redis
- **Monitoring**: Prometheus + Node Exporter

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

# Run Worker (in another terminal)
python3 -m src.worker

```

### Docker Compose (Full Stack)

```bash
# Start all services
docker compose up

# API: http://localhost:8000
# Grafana: http://localhost:3000
# Prometheus: http://localhost:9090

```

### Kubernetes Deployment

```bash
# Deploy everything (including infrastructure)
kubectl apply -f k8s/ -n default

# Or use Helm
helm install testing ./helm/testing \
  --namespace default \
  --create-namespace
```

## 📁 Project Structure

```
testing/
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

- **Metrics**: http://localhost:8000/metrics
- **Node Metrics**: http://localhost:9100/metrics
- **Prometheus**: http://localhost:9090
- **Grafana**: http://localhost:3000 (admin/admin)

## 📚 Documentation

- [Deployment Guide](docs/DEPLOYMENT.md)
- [Development Guide](docs/DEVELOPMENT.md)
- [API Documentation](http://localhost:8000/docs) (when running)

## 👤 Author

MatanGilat <matangilat@koaa.io>

## 📄 License

MIT
