# Testing the Cookiecutter Template - Step by Step Guide

## 🚀 Quick Start (Automated)

Run the automated test script:

```bash
cd /home/matan/projects/cookiecutter-microservice
./test_and_setup.sh
```

This will:
1. ✅ Generate a test project
2. ✅ Create a virtual environment
3. ✅ Install all dependencies
4. ✅ Verify no syntax errors
5. ✅ Run tests

---

## 📋 Manual Step-by-Step Instructions

### Step 0: System Prerequisites (Debian/Ubuntu)

```bash
# Install required system packages (one-time setup)
sudo apt-get update
sudo apt-get install -y python3 python3-venv python3-pip pipx git build-essential

# Setup pipx path
pipx ensurepath

# Verify installation
python3 --version
```

### Step 1: Install Cookiecutter

```bash
# Install cookiecutter with pipx (recommended for Debian/Ubuntu)
pipx install cookiecutter

# Close and reopen terminal, then verify
cookiecutter --version
```

### Step 2: Generate a Test Project

```bash
# Navigate to workspace
cd /home/matan/projects

# Generate project with default settings
cookiecutter cookiecutter-microservice --no-input

# Or with custom settings (interactive)
cookiecutter cookiecutter-microservice
```

### Step 3: Create Virtual Environment

```bash
# Navigate to generated project
cd my-microservice

# Create venv
python3 -m venv venv

# Activate it
source venv/bin/activate

# Verify activation (should show venv path)
which python
```

### Step 4: Install Dependencies

```bash
# Upgrade pip first
pip install --upgrade pip

# Install production dependencies
pip install -r requirements.txt

# Install development dependencies (optional)
pip install -r requirements-dev.txt
```

### Step 5: Verify Installation

```bash
# Check for syntax errors
python -m py_compile src/*.py

# Or use flake8
flake8 src/ --extend-ignore=E501,W503

# Or just try importing
python -c "from src import config; print('✅ Imports work!')"
```

### Step 6: Run the Application

```bash
# Run FastAPI app
python -m src.app_fastapi

# App will be at: http://localhost:8000
# Docs at: http://localhost:8000/docs
# Health: http://localhost:8000/healthz
```

### Step 7: Run Tests

```bash
# Run all tests
pytest

# With coverage
pytest --cov=src --cov-report=html

# View coverage report
open htmlcov/index.html
```

### Step 8: Try Docker Compose

```bash
# Start full stack (if infrastructure is deployed)
docker compose up -d

# View logs
docker compose logs -f api

# Stop everything
docker compose down
```

---

## 🎯 Testing Different Configurations

### Test with Flask Instead of FastAPI

```bash
cd /home/matan/projects

cookiecutter cookiecutter-microservice \
  --no-input \
  project_name="flask-test" \
  web_framework=flask

cd flask-test
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m src.app_flask
```

### Test with MongoDB

```bash
cd /home/matan/projects

cookiecutter cookiecutter-microservice \
  --no-input \
  project_name="mongo-test" \
  database_type=mongodb \
  deploy_database=yes

cd mongo-test
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Test with Full Infrastructure

```bash
cd /home/matan/projects

cookiecutter cookiecutter-microservice \
  --no-input \
  project_name="full-stack-test" \
  database_type=postgresql \
  deploy_database=yes \
  queue_type=kafka \
  deploy_queue=yes \
  cache_type=redis \
  deploy_cache=yes \
  deploy_monitoring_stack=yes

cd full-stack-test
docker compose up -d
```

### Test Minimal (No Dependencies)

```bash
cd /home/matan/projects

cookiecutter cookiecutter-microservice \
  --no-input \
  project_name="minimal-test" \
  database_type=none \
  queue_type=none \
  cache_type=none \
  use_async_workers=no

cd minimal-test
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m src.app_fastapi
```

---

## 🐛 Troubleshooting

### Issue: "cookiecutter: command not found"

```bash
# Install cookiecutter
pip install cookiecutter

# Or add to PATH if using pipx
export PATH="$HOME/.local/bin:$PATH"
```

### Issue: "No module named 'pydantic_settings'"

```bash
# Make sure venv is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### Issue: "Port 8000 already in use"

```bash
# Find and kill process
lsof -ti:8000 | xargs kill -9

# Or use different port
PORT=8001 python -m src.app_fastapi
```

### Issue: Docker compose fails

```bash
# Check if Docker is running
docker ps

# View logs
docker-compose logs

# Rebuild images
docker-compose build --no-cache
```

---

## 📊 What to Check in Generated Project

### ✅ Project Structure

```bash
tree -L 2 -I 'venv|__pycache__'
```

Should show:
- `src/` directory with all modules
- `k8s/` with Kubernetes manifests
- `tests/` directory
- `requirements.txt` (customized based on choices)
- `docker-compose.yaml` (with selected services)

### ✅ No Template Syntax

```bash
# Should NOT see any Jinja2 syntax like {% if %} or {{ }}
grep -r "{% " src/
grep -r "{{ " src/

# Should return nothing (empty)
```

### ✅ Dependencies Match Choices

```bash
# Check requirements based on what you selected
cat requirements.txt

# If you chose FastAPI, should see:
# fastapi>=0.104.0

# If you chose PostgreSQL, should see:
# asyncpg>=0.29.0
```

### ✅ Valid Python

```bash
# Compile all Python files
python -m compileall src/

# Should succeed with no errors
```

---

## 🎯 Performance Test

```bash
# Install load testing tool
pip install locust

# Create simple test
cat > locustfile.py << 'EOF'
from locust import HttpUser, task

class QuickstartUser(HttpUser):
    @task
    def health_check(self):
        self.client.get("/healthz")
    
    @task
    def readiness_check(self):
        self.client.get("/ready")
EOF

# Run app
python -m src.app_fastapi &

# Run load test (1000 users, 100/sec spawn rate)
locust -f locustfile.py --headless -u 1000 -r 100 -t 30s --host http://localhost:8000
```

---

## 📝 Summary of Commands

```bash
# 1. Generate project
cd /home/matan/projects
cookiecutter cookiecutter-microservice --no-input

# 2. Setup venv
cd my-microservice
python3 -m venv venv
source venv/bin/activate

# 3. Install deps
pip install -r requirements.txt

# 4. Run app
python -m src.app_fastapi

# 5. Test it
curl http://localhost:8000/healthz
```

Done! Your microservice should be running at http://localhost:8000 🚀
