#!/bin/bash
# System setup script for Debian/Ubuntu
# Run this once before using the cookiecutter template

set -e

echo "🔧 Setting up system for Cookiecutter Microservice Template"
echo "============================================================"
echo ""

# Check if running on Debian/Ubuntu
if ! command -v apt-get &> /dev/null; then
    echo "⚠️  This script is for Debian/Ubuntu systems only"
    echo "   For other systems, install python3, python3-venv, and pip manually"
    exit 1
fi

echo "📦 Installing system packages..."
sudo apt-get update
sudo apt-get install -y \
    python3 \
    python3-venv \
    python3-pip \
    git \
    curl \
    build-essential

echo ""
echo "🐍 Installing pipx and cookiecutter..."
sudo apt-get install -y pipx
pipx ensurepath

# Install cookiecutter with pipx
pipx install cookiecutter

echo ""
echo "✅ System setup complete!"
echo ""
echo "📝 Verify installation:"
python3 --version
cookiecutter --version
echo ""
echo "⚠️  IMPORTANT: Close and reopen your terminal, then run:"
echo "   cd /home/matan/projects"
echo "   cookiecutter cookiecutter-microservice"
echo ""
