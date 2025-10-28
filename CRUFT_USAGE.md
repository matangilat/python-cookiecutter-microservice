# Using Cruft to Manage Template Updates

[Cruft](https://github.com/cruft/cruft) is a tool that allows you to maintain and update projects generated from cookiecutter templates. It's the **recommended way** to keep your microservices up-to-date with template changes.

## Installation

```bash
# Using pip
pip install cruft

# Using pipx (recommended)
pipx install cruft
```

## Creating a New Project with Cruft

Instead of using `cookiecutter`, use `cruft create`:

```bash
# Create a new project
cruft create https://github.com/matangilat/python-cookiecutter-microservice

# Or from local path
cruft create /path/to/cookiecutter-microservice
```

This creates the project and adds a `.cruft.json` file that tracks:
- Template URL
- Template version/commit
- Your configuration answers

## Updating an Existing Project

### Check for Updates

```bash
cd your-microservice
cruft check
```

This will tell you if the template has updates available.

### Update Your Project

```bash
cd your-microservice
cruft update
```

Cruft will:
1. Re-generate the template with your saved configuration
2. Compare changes between old and new versions
3. Apply updates while preserving your custom changes
4. Show you conflicts that need manual resolution

### Update with Specific Options

```bash
# Skip files that would cause conflicts
cruft update --skip-apply-ask

# Update to a specific template version
cruft update --checkout main

# Update to a specific commit
cruft update --checkout abc123

# Interactive update (review each change)
cruft update --skip-apply-ask
```

## Converting an Existing Cookiecutter Project to Cruft

If you created a project with `cookiecutter` and want to start using `cruft`:

```bash
cd your-existing-microservice

# Link the project to the template
cruft link https://github.com/matangilat/python-cookiecutter-microservice
```

You'll be prompted to confirm your original configuration values. Cruft will create a `.cruft.json` file.

## Example Workflow

### Initial Creation

```bash
# Create a new microservice with cruft
cruft create https://github.com/matangilat/python-cookiecutter-microservice

# Answer the prompts
# project_name: payment-service
# web_framework: fastapi
# database_type: postgresql
# enable_node_exporter: yes
# ...

cd payment-service
git init
git add .
git commit -m "Initial project from template"
```

### Later Updates

```bash
cd payment-service

# Check if template has updates
cruft check

# If updates available:
# ✓ Template is up to date
# or
# ✗ Template has updates available

# Update your project
cruft update

# Review changes
git diff

# Commit if good
git add .
git commit -m "Update from template: add Grafana dashboards"
```

## Benefits of Using Cruft

1. **Track Template Changes** - Know when the template is updated
2. **Easy Updates** - One command to pull in template improvements
3. **Preserve Custom Changes** - Your modifications are kept
4. **Version Control Friendly** - Works well with git
5. **Reproducible** - `.cruft.json` documents your configuration

## Best Practices

### 1. Always Use Git

```bash
# Before updating
git status  # Make sure working directory is clean
git checkout -b update-template

# After updating
git diff    # Review changes
git add .
git commit -m "Update from template"
```

### 2. Review Changes Carefully

```bash
# After cruft update, review:
git diff

# Look for:
# - New features you want to keep
# - Changes that might break your custom code
# - Configuration updates
```

### 3. Handle Conflicts

If cruft finds conflicts:

```bash
# Cruft will show conflict markers like:
# <<<<<<< Updated
# New template code
# =======
# Your custom code
# >>>>>>> Current

# Manually resolve in your editor
# Then commit the resolved version
```

### 4. Test After Updates

```bash
# After updating, always test
cruft update

# Run tests
make test

# Try running locally
docker-compose up -d
```

## Common Commands

```bash
# Create new project
cruft create <template-url>

# Check for template updates
cruft check

# Update project from template
cruft update

# Link existing project to template
cruft link <template-url>

# Show current template information
cruft diff

# Update to specific version
cruft update --checkout <branch-or-commit>
```

## .cruft.json Example

After creating with cruft, you'll have a `.cruft.json` file:

```json
{
  "template": "https://github.com/matangilat/python-cookiecutter-microservice",
  "commit": "abc123def456",
  "checkout": null,
  "context": {
    "cookiecutter": {
      "project_name": "payment-service",
      "project_slug": "payment-service",
      "project_description": "Payment processing microservice",
      "author_name": "John Doe",
      "author_email": "john@example.com",
      "web_framework": "fastapi",
      "database_type": "postgresql",
      "deploy_database": "yes",
      "queue_type": "kafka",
      "deploy_queue": "yes",
      "cache_type": "redis",
      "deploy_cache": "yes",
      "enable_metrics": "yes",
      "enable_node_exporter": "yes",
      "enable_tracing": "yes",
      "deploy_monitoring_stack": "yes",
      "use_async_workers": "yes",
      "python_version": "3.11",
      "docker_registry": "ghcr.io/yourorg",
      "kubernetes_namespace": "default",
      "include_ci_cd": "github-actions"
    }
  },
  "directory": null
}
```

**Commit this file to git!** It ensures reproducible builds and enables updates.

## Updating Multiple Microservices

If you have many microservices from the same template:

```bash
#!/bin/bash
# update-all-services.sh

SERVICES=(
  "payment-service"
  "user-service"
  "notification-service"
)

for service in "${SERVICES[@]}"; do
  echo "Updating $service..."
  cd "$service"
  
  if cruft check; then
    echo "✓ $service is up to date"
  else
    echo "Updating $service..."
    cruft update --skip-apply-ask
    
    # Review and commit manually
    git diff
  fi
  
  cd ..
done
```

## Troubleshooting

### "Project was not created from a Cruft template"

```bash
# Link the project to the template
cruft link https://github.com/matangilat/python-cookiecutter-microservice
```

### Update Creates Too Many Conflicts

```bash
# Do a dry run first
cruft diff

# Update without applying
cruft update --skip-apply-ask

# Manually merge important changes
```

### Want to Skip Certain Files

Edit `.cruft.json` to add skip patterns:

```json
{
  "skip": [
    "README.md",
    "custom-config.yaml"
  ]
}
```

## Resources

- [Cruft Documentation](https://cruft.github.io/cruft/)
- [Cruft GitHub](https://github.com/cruft/cruft)
- [Cookiecutter Documentation](https://cookiecutter.readthedocs.io/)

## Recommendation

✅ **Use Cruft for all new microservices**  
✅ **Convert existing projects with `cruft link`**  
✅ **Commit `.cruft.json` to version control**  
✅ **Regularly check for template updates**
