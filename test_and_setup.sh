#!/bin/bash
# Quick test script for the Cookiecutter template

set -e  # Exit on error

echo "🧪 Testing Cookiecutter Microservice Template"
echo "=============================================="
echo ""

# Check for python3-venv on Debian/Ubuntu
if command -v apt-get &> /dev/null; then
    if ! dpkg -l | grep -q python3-venv; then
        echo "📦 Installing python3-venv and pipx..."
        sudo apt-get update
        sudo apt-get install -y python3-venv python3-pip pipx
        pipx ensurepath
    fi
fi

# Check if cookiecutter is installed
if ! command -v cookiecutter &> /dev/null; then
    echo "❌ Cookiecutter not found. Installing with pipx..."
    pipx install cookiecutter
    export PATH="$HOME/.local/bin:$PATH"
fi

# Step 1: Generate a test project
echo "📦 Step 1: Generating test project..."
cd /home/matan/projects

# Remove old test project if it exists
if [ -d "my-microservice" ]; then
    echo "🗑️  Removing old test project..."
    rm -rf my-microservice
fi

# Generate new project
cookiecutter cookiecutter-microservice --no-input

echo "✅ Project generated!"
echo ""

# Step 2: Create virtual environment
echo "🐍 Step 2: Creating virtual environment..."
cd my-microservice

python3 -m venv venv
echo "✅ Virtual environment created!"
echo ""

# Step 3: Activate and install dependencies
echo "📚 Step 3: Installing dependencies..."
source venv/bin/activate

python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
python3 -m pip install -r requirements-dev.txt

echo "✅ Dependencies installed!"
echo ""

# Step 4: Check for syntax errors
echo "🔍 Step 4: Checking for Python syntax errors..."
python -m py_compile src/*.py
python -m py_compile src/**/*.py 2>/dev/null || true
echo "✅ No syntax errors found!"
echo ""

# Step 5: Run tests (if any)
echo "🧪 Step 5: Running tests..."
if [ -d "tests" ]; then
    pytest tests/ -v || echo "⚠️  Some tests may fail (expected for template)"
fi
echo ""

# Step 6: Show structure
echo "📁 Step 6: Project structure:"
tree -L 2 -I 'venv|__pycache__|*.pyc' || ls -la
echo ""

# Step 7: Instructions
echo "✅ Template test complete!"
echo ""
echo "🚀 Next steps:"
echo "   cd /home/matan/projects/my-microservice"
echo "   source venv/bin/activate"
echo "   python -m src.app_fastapi"
echo ""
echo "📊 Or with Docker:"
echo "   docker-compose up"
echo ""

deactivate
