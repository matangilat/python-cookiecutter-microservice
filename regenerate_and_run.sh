#!/bin/bash
set -e

echo "🗑️  Removing old project..."
cd /home/matan/projects
rm -rf my-microservice

echo "🔧 Generating new project..."
cookiecutter ./cookiecutter-microservice --no-input

echo "📦 Setting up virtual environment..."
cd my-microservice
python3 -m venv venv

echo "📚 Installing dependencies..."
./venv/bin/pip install -q -r requirements.txt

echo "✅ Setup complete! Starting server..."
echo "🌐 Server will be at http://localhost:8000"
echo "📖 API docs will be at http://localhost:8000/docs"
echo ""
./venv/bin/uvicorn src.app_fastapi:app --host 0.0.0.0 --port 8000 --reload
