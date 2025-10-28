# Cookiecutter Microservice Template

A production-ready, highly configurable Kubernetes microservice template with pluggable infrastructure.

## ✨ Features

- **🎯 Multiple Frameworks**: Choose between FastAPI or Flask
- **💾 Database Options**: PostgreSQL, MySQL, MongoDB, or none
- **📮 Queue Options**: Kafka, RabbitMQ, SQS, or none  
- **🗄️ Cache Options**: Redis, Memcached, or none
- **🚀 Deploy Infrastructure**: Optionally deploy databases, queues, and caches with your service
- **📊 Monitoring**: Prometheus, Grafana, and node-exporter support
- **🐳 Kubernetes Ready**: Complete manifests with health probes, HPA, and ingress
- **⚙️ CI/CD**: GitHub Actions or GitLab CI pipelines
- **🧪 Testing**: Pre-configured pytest with async support
- **📚 Clean Architecture**: Proper separation of concerns (API, Services, Repositories)

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- [Cookiecutter](https://github.com/cookiecutter/cookiecutter)

### Installation

**On Debian/Ubuntu (recommended):**
```bash
# Install system packages
sudo apt-get update
sudo apt-get install -y python3 python3-venv pipx

# Install cookiecutter with pipx
pipx install cookiecutter
pipx ensurepath

# Close and reopen terminal
```

**Other systems:**
```bash
pip install cookiecutter

# Generate a new microservice
cookiecutter https://github.com/yourorg/cookiecutter-microservice

# Or from local path
cookiecutter /path/to/cookiecutter-microservice
```

### Interactive Prompts

You'll be asked:

```
project_name [my-microservice]: payment-service
project_description [...]: Payment processing microservice
author_name [Your Name]: John Doe
author_email [your.email@example.com]: john@example.com

Select web_framework:
1 - fastapi
2 - flask
Choose from 1, 2 [1]: 1

Select database_type:
1 - postgresql
2 - mysql
3 - mongodb
4 - none
Choose from 1, 2, 3, 4 [1]: 1

Select deploy_database:
1 - yes
2 - no
Choose from 1, 2 [1]: 1

Select queue_type:
1 - kafka
2 - rabbitmq
3 - sqs
4 - none
Choose from 1, 2, 3, 4 [1]: 1

...
```

## 📁 Generated Project Structure

```
my-microservice/
├── src/
│   ├── api/                    # API routes
│   │   ├── routes/            # FastAPI routes
│   │   └── routes_flask/      # Flask blueprints
│   ├── models/
│   │   ├── entities.py        # Database models
│   │   └── schemas.py         # Pydantic schemas
│   ├── services/              # Business logic
│   ├── repositories/          # Data access layer
│   ├── infrastructure/        # External integrations
│   │   ├── database.py
│   │   ├── cache.py
│   │   ├── queue.py
│   │   └── metrics.py
│   └── utils/                 # Utilities
├── k8s/
│   ├── infrastructure/        # Optional infra deployments
│   │   ├── database/
│   │   ├── queue/
│   │   └── cache/
│   ├── monitoring/            # Prometheus, Grafana
│   ├── api-deployment.yaml
│   ├── worker-deployment.yaml
│   └── service.yaml
├── tests/
├── config/
│   └── infrastructure.yaml
├── docker-compose.yaml
├── Dockerfile
├── Makefile
└── README.md
```

## 🎨 Configuration Options

### Web Framework

- **FastAPI**: Modern, fast, auto-docs with OpenAPI
- **Flask**: Mature, flexible, widely adopted

### Database

- **PostgreSQL**: ACID compliant, feature-rich
- **MySQL**: Popular, widely supported
- **MongoDB**: Document database, flexible schema
- **None**: Stateless service

### Message Queue

- **Kafka**: High throughput, distributed streaming
- **RabbitMQ**: Flexible routing, AMQP protocol
- **SQS**: AWS managed queue service
- **None**: No async processing

### Cache

- **Redis**: In-memory, pub/sub, persistence
- **Memcached**: Simple, fast, memory cache
- **None**: No caching layer

### Infrastructure Deployment

- **Deploy with service**: StatefulSets for DB/queue/cache
- **Use external**: Connect to existing infrastructure

### Monitoring

- **Prometheus**: Metrics collection
- **Grafana**: Visualization dashboards
- **Node Exporter**: Host-level metrics (CPU, memory, disk)

## 🛠️ Development Workflow

```bash
# 1. Generate project
cookiecutter cookiecutter-microservice

# 2. Navigate to project
cd my-microservice

```bash
# On Debian/Ubuntu, install venv first
sudo apt-get update && sudo apt-get install -y python3-venv python3-pip

# Create virtual environment and install dependencies
python3 -m venv venv
source venv/bin/activate
python3 -m pip install -r requirements.txt

# Run locally
python3 -m src.main  # or src.app_fastapi / src.app_flask

# Run tests
python3 -m pytest

# Run with Docker Compose
docker compose up

# Deploy to Kubernetes
kubectl apply -f k8s/ -n default
```
```

## 📊 Architecture Patterns

### Clean Architecture Layers

1. **API Layer** (`src/api/`): HTTP endpoints, request/response handling
2. **Service Layer** (`src/services/`): Business logic, orchestration
3. **Repository Layer** (`src/repositories/`): Data access, CRUD operations
4. **Infrastructure Layer** (`src/infrastructure/`): External services (DB, cache, queue)
5. **Models** (`src/models/`): Domain entities and schemas

### Dependency Flow

```
API → Services → Repositories → Infrastructure
```

All dependencies flow inward. Inner layers don't know about outer layers.

## 🔒 Security Features

- Non-root container user
- Security contexts in Kubernetes
- Read-only root filesystem
- Resource limits
- Secret management
- Network policies (optional)

## 📈 Scalability

- Horizontal Pod Autoscaling (HPA)
- Stateless API design
- Async workers for background jobs
- Connection pooling
- Caching strategies

## 🔍 Observability

- **Metrics**: Prometheus endpoints (`/metrics`)
- **Health Checks**: Liveness (`/healthz`) and readiness (`/ready`)
- **Structured Logging**: JSON logs to stdout
- **Distributed Tracing**: OpenTelemetry support (optional)

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details

## 🙏 Acknowledgments

Built with:
- [Cookiecutter](https://github.com/cookiecutter/cookiecutter)
- [FastAPI](https://fastapi.tiangolo.com/) / [Flask](https://flask.palletsprojects.com/)
- [Kubernetes](https://kubernetes.io/)
- [Prometheus](https://prometheus.io/)

## 📚 Documentation

After generation, see:
- `docs/DEPLOYMENT.md` - Kubernetes deployment guide
- `docs/DEVELOPMENT.md` - Local development guide
- `docs/INFRASTRUCTURE.md` - Infrastructure catalog details
- `docs/USAGE.md` - Customization examples

## 💡 Examples

### Minimal Stateless API

```bash
cookiecutter cookiecutter-microservice \
  --no-input \
  project_name="my-api" \
  web_framework=fastapi \
  database_type=none \
  queue_type=none \
  cache_type=none \
  deploy_monitoring_stack=no

cd my-api
python3 -m venv venv
source venv/bin/activate
python3 -m pip install -r requirements.txt
python3 -m src.app_fastapi
```

### Full-Stack Service with Infrastructure

```bash
cookiecutter cookiecutter-microservice \
  --no-input \
  project_name="order-service" \
  web_framework=fastapi \
  database_type=postgresql \
  deploy_database=yes \
  queue_type=kafka \
  deploy_queue=yes \
  cache_type=redis \
  deploy_cache=yes \
  enable_node_exporter=yes \
  deploy_monitoring_stack=yes
```

## 🆘 Support

- Issues: https://github.com/yourorg/cookiecutter-microservice/issues
- Discussions: https://github.com/yourorg/cookiecutter-microservice/discussions

---

**Happy coding! 🚀**
