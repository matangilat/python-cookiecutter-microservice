# Cookiecutter Microservice Template - Quick Reference

## Generate a New Service

```bash
cookiecutter cookiecutter-microservice
```

## Configuration Choices

| Option | Values | Description |
|--------|--------|-------------|
| `web_framework` | `fastapi`, `flask` | Web framework |
| `database_type` | `postgresql`, `mysql`, `mongodb`, `none` | Database |
| `deploy_database` | `yes`, `no` | Deploy DB with service |
| `queue_type` | `kafka`, `rabbitmq`, `sqs`, `none` | Message queue |
| `deploy_queue` | `yes`, `no` | Deploy queue with service |
| `cache_type` | `redis`, `memcached`, `none` | Cache layer |
| `deploy_cache` | `yes`, `no` | Deploy cache with service |
| `enable_metrics` | `yes`, `no` | Prometheus metrics |
| `enable_node_exporter` | `yes`, `no` | Host metrics |
| `deploy_monitoring_stack` | `yes`, `no` | Prometheus + Grafana |
| `use_async_workers` | `yes`, `no` | Background workers |
| `include_ci_cd` | `github-actions`, `gitlab-ci`, `none` | CI/CD pipeline |

## Non-Interactive Mode

```bash
cookiecutter cookiecutter-microservice \
  --no-input \
  project_name="my-service" \
  web_framework=fastapi \
  database_type=postgresql \
  deploy_database=yes
```

## Post-Generation Steps

```bash
# Install venv (Debian/Ubuntu only - one-time setup)
sudo apt-get update && sudo apt-get install -y python3-venv python3-pip

# Setup project
cd my-service
python3 -m src.app_fastapi

# Or with Docker
docker compose up
```

## Common Recipes

### Stateless API (No Dependencies)
```bash
cookiecutter . --no-input database_type=none queue_type=none cache_type=none
```

### Full Microservice + Infrastructure
```bash
cookiecutter . --no-input deploy_database=yes deploy_queue=yes deploy_cache=yes deploy_monitoring_stack=yes
```

### Flask with MongoDB
```bash
cookiecutter . --no-input web_framework=flask database_type=mongodb
```

## Project Structure

```
generated-service/
├── src/
│   ├── api/              # Endpoints
│   ├── services/         # Business logic
│   ├── repositories/     # Data access
│   ├── models/          # Schemas & entities
│   └── infrastructure/  # External clients
├── k8s/                 # Kubernetes manifests
├── tests/               # Test suite
├── docker-compose.yaml  # Local development
└── Makefile            # Common tasks
```

## Key Files

- `config/infrastructure.yaml` - Infrastructure configuration
- `src/app_fastapi.py` or `src/app_flask.py` - Application entry point
- `src/worker.py` - Background worker (if enabled)
- `.env.example` - Environment variables template

## Make Commands

```bash
make help            # Show all commands
make install         # Install dependencies
make run             # Run API locally
make test            # Run tests
make docker-build    # Build Docker image
make docker-up       # Start with docker-compose
make k8s-deploy      # Deploy to Kubernetes
```

## Endpoints

- `http://localhost:8000/` - API root
- `http://localhost:8000/docs` - FastAPI docs (Swagger)
- `http://localhost:8000/healthz` - Health check
- `http://localhost:8000/ready` - Readiness check
- `http://localhost:8000/metrics` - Prometheus metrics

## Monitoring (if enabled)

- `http://localhost:9090` - Prometheus
- `http://localhost:3000` - Grafana (admin/admin)
- `http://localhost:9100/metrics` - Node exporter

## Next Steps

1. ✅ Customize `config/infrastructure.yaml`
2. ✅ Add your business logic to `src/services/`
3. ✅ Create API endpoints in `src/api/routes/`
4. ✅ Write tests in `tests/`
5. ✅ Update secrets in `k8s/secret.yaml`
6. ✅ Deploy: `kubectl apply -f k8s/`
