#!/usr/bin/env python3
"""
Post-generation hook for cookiecutter template.
This runs after the project is generated to clean up and customize based on user choices.
"""
import os
import shutil
from pathlib import Path

PROJECT_DIRECTORY = Path.cwd()


def remove_file(filepath):
    """Remove a file."""
    file_path = PROJECT_DIRECTORY / filepath
    if file_path.exists():
        file_path.unlink()


def remove_dir(dirpath):
    """Remove a directory."""
    dir_path = PROJECT_DIRECTORY / dirpath
    if dir_path.exists():
        shutil.rmtree(dir_path)


def main():
    """Main post-generation logic."""
    
    # Get cookiecutter config
    web_framework = "{{ cookiecutter.web_framework }}"
    database_type = "{{ cookiecutter.database_type }}"
    deploy_database = "{{ cookiecutter.deploy_database }}"
    queue_type = "{{ cookiecutter.queue_type }}"
    deploy_queue = "{{ cookiecutter.deploy_queue }}"
    cache_type = "{{ cookiecutter.cache_type }}"
    deploy_cache = "{{ cookiecutter.deploy_cache }}"
    use_async_workers = "{{ cookiecutter.use_async_workers }}"
    deploy_monitoring = "{{ cookiecutter.deploy_monitoring_stack }}"
    include_ci_cd = "{{ cookiecutter.include_ci_cd }}"
    
    print("🔧 Customizing your microservice...")
    
    # Remove unused web framework
    if web_framework == "fastapi":
        remove_file("src/app_flask.py")
        print("✓ Using FastAPI")
    else:
        remove_file("src/app_fastapi.py")
        print("✓ Using Flask")
    
    # Clean up database files
    if database_type == "none":
        remove_file("src/infrastructure/database.py")
        remove_file("src/repositories/base_repository.py")
        print("✓ No database configured")
    else:
        print(f"✓ Using {database_type}")
    
    # Clean up queue files
    if queue_type == "none" or use_async_workers == "no":
        remove_file("src/worker.py")
        remove_file("k8s/worker-deployment.yaml")
        print("✓ No worker configured")
    else:
        print(f"✓ Using {queue_type} with workers")
    
    # Clean up infrastructure deployments
    if deploy_database == "no":
        remove_dir("k8s/infrastructure/database")
        print("✓ Using external database")
    
    if deploy_queue == "no":
        remove_dir("k8s/infrastructure/queue")
        print("✓ Using external queue")
    
    if deploy_cache == "no":
        remove_dir("k8s/infrastructure/cache")
        print("✓ Using external cache")
    
    if deploy_monitoring == "no":
        remove_dir("k8s/monitoring")
        print("✓ Using external monitoring")
    
    # Clean up CI/CD files
    if include_ci_cd == "github-actions":
        remove_file(".gitlab-ci.yml")
        print("✓ Using GitHub Actions")
    elif include_ci_cd == "gitlab-ci":
        remove_dir(".github")
        print("✓ Using GitLab CI")
    else:
        remove_dir(".github")
        remove_file(".gitlab-ci.yml")
        print("✓ No CI/CD configured")
    
    print("\n✅ Microservice template generated successfully!")
    print(f"📁 Project: {PROJECT_DIRECTORY.name}")
    print(f"🌐 Framework: {web_framework}")
    print(f"💾 Database: {database_type}")
    print(f"📮 Queue: {queue_type}")
    print(f"🗄️  Cache: {cache_type}")
    print("\n🚀 Next steps:")
    print("   # On Debian/Ubuntu (one-time setup):")
    print("   sudo apt-get update && sudo apt-get install -y python3-venv python3-pip")
    print("")
    print("   # Setup project:")
    print("   cd {{ cookiecutter.project_slug }}")
    print("   python3 -m venv venv")
    print("   source venv/bin/activate")
    print("   python3 -m pip install -r requirements.txt")
    print("   python3 -m src.app_{{ cookiecutter.web_framework }}")
    print("\n   Or with Docker:")
    print("   docker compose up")


if __name__ == "__main__":
    main()
