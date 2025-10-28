#!/usr/bin/env python3
"""
Test script to verify the Cookiecutter template generates valid projects.
This should be run from the cookiecutter-microservice directory.
"""
import subprocess
import sys
import tempfile
import shutil
from pathlib import Path


def test_template_generation():
    """Test generating a project with the template."""
    
    # Create temporary directory for test
    with tempfile.TemporaryDirectory() as tmpdir:
        print(f"🧪 Testing template generation in {tmpdir}")
        
        # Generate project with default values
        cmd = [
            "cookiecutter",
            ".",
            "--no-input",
            "--output-dir", tmpdir,
        ]
        
        try:
            result = subprocess.run(cmd, check=True, capture_output=True, text=True)
            print("✅ Template generated successfully!")
            
            # Check if project directory was created
            project_dir = Path(tmpdir) / "my-microservice"
            if not project_dir.exists():
                print("❌ Project directory not created")
                return False
            
            print(f"✅ Project directory created: {project_dir}")
            
            # Check for key files
            key_files = [
                "src/app_fastapi.py",
                "src/config.py",
                "requirements.txt",
                "Dockerfile",
                "docker-compose.yaml",
                "k8s/api-deployment.yaml",
                "README.md",
            ]
            
            for file_path in key_files:
                full_path = project_dir / file_path
                if full_path.exists():
                    print(f"✅ Found: {file_path}")
                else:
                    print(f"❌ Missing: {file_path}")
                    return False
            
            # Check if Flask file was removed (since FastAPI is default)
            flask_file = project_dir / "src/app_flask.py"
            if not flask_file.exists():
                print("✅ Flask file correctly removed (FastAPI selected)")
            else:
                print("⚠️  Flask file still present (should be removed)")
            
            # Try to parse a Python file to verify it's valid
            config_file = project_dir / "src/config.py"
            try:
                import ast
                with open(config_file, 'r') as f:
                    ast.parse(f.read())
                print(f"✅ Generated Python is syntactically valid: {config_file.name}")
            except SyntaxError as e:
                print(f"❌ Generated Python has syntax errors: {e}")
                return False
            
            print("\n🎉 All tests passed! Template is working correctly.")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Template generation failed: {e}")
            print(f"STDOUT: {e.stdout}")
            print(f"STDERR: {e.stderr}")
            return False


if __name__ == "__main__":
    # Check if cookiecutter is installed
    try:
        subprocess.run(["cookiecutter", "--version"], check=True, capture_output=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Cookiecutter is not installed. Install it with: pip install cookiecutter")
        sys.exit(1)
    
    # Run tests
    success = test_template_generation()
    sys.exit(0 if success else 1)
