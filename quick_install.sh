#!/bin/bash
# Quick one-liner setup for Debian/Ubuntu

echo "🚀 Quick Setup for Cookiecutter Microservice Template (Debian/Ubuntu)"
echo "======================================================================"

# Install everything needed
sudo apt-get update && \
sudo apt-get install -y python3 python3-venv python3-pip pipx git build-essential && \
pipx install cookiecutter && \
pipx ensurepath

echo ""
echo "✅ Installation complete!"
echo ""
echo "⚠️  IMPORTANT: You must close and reopen your terminal for cookiecutter to be available"
echo ""
echo "Then run:"
echo "  cd /home/matan/projects"
echo "  cookiecutter cookiecutter-microservice"
