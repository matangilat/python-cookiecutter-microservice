# Template Structure Migration Guide

## Overview

The cookiecutter template has been restructured to provide better separation of concerns with clear boundaries between API, Classes, Utils, and Tests.

## New Structure

```
src/
├── api/                    # All API-related code
│   ├── routes/            # FastAPI routes
│   └── routes_flask/      # Flask blueprints
├── classes/                # Business logic and domain models
│   ├── models/            # Data models
│   │   ├── entities.py    # Database entities
│   │   └── schemas.py     # API schemas (Pydantic)
│   ├── services/          # Business logic layer
│   │   └── item_service.py
│   └── repositories/      # Data access layer
│       ├── base_repository.py
│       └── item_repository.py
├── utils/                  # Utilities and infrastructure
│   ├── logging.py
│   ├── cache.py
│   ├── database.py
│   └── metrics.py
└── tests/                  # All tests
    ├── unit/
    └── integration/
```

## What Changed

### 1. **API Layer** (`src/api/`)
- **No changes** - Routes and endpoints remain in the same location
- Still separated by framework (routes/ for FastAPI, routes_flask/ for Flask)

### 2. **Classes** (`src/classes/`) - NEW
Previously split across multiple directories, now consolidated:
- `src/models/` → `src/classes/models/`
- `src/services/` → `src/classes/services/`
- `src/repositories/` → `src/classes/repositories/`

### 3. **Utils** (`src/utils/`)
- **Absorbed infrastructure**: `src/infrastructure/` → `src/utils/`
- Now contains: logging, cache, database, metrics
- All helper functions and infrastructure clients

### 4. **Tests** (`src/tests/`) - MOVED
- `tests/` (root level) → `src/tests/`
- Better organization with subdirectories:
  - `src/tests/unit/` - Unit tests
  - `src/tests/integration/` - Integration tests

## Migration Steps for Existing Projects

If you've already generated a project from the old template:

### Option 1: Restructure Manually

1. **Create new directories:**
   ```bash
   mkdir -p src/classes/{models,services,repositories}
   mkdir -p src/tests/{unit,integration}
   ```

2. **Move files:**
   ```bash
   # Move models
   mv src/models/* src/classes/models/
   
   # Move services
   mv src/services/* src/classes/services/
   
   # Move repositories
   mv src/repositories/* src/classes/repositories/
   
   # Move infrastructure to utils
   mv src/infrastructure/* src/utils/
   
   # Move tests
   mv tests/* src/tests/
   ```

3. **Update imports** in all Python files:
   - `from src.models` → `from src.classes.models`
   - `from src.services` → `from src.classes.services`
   - `from src.repositories` → `from src.classes.repositories`
   - `from src.infrastructure` → `from src.utils`

4. **Update configuration files:**
   - Update `Makefile` test path: `pytest tests/` → `pytest src/tests/`
   - Update any CI/CD configs that reference old paths

5. **Clean up old directories:**
   ```bash
   rmdir src/models src/services src/repositories src/infrastructure
   rmdir tests
   ```

### Option 2: Regenerate from Template

1. Back up your custom code
2. Regenerate project with updated cookiecutter
3. Port your custom code to new structure

## Benefits of New Structure

✅ **Clear Separation**: Each directory has a single, well-defined purpose
✅ **Better Discoverability**: Easy to find API vs business logic vs utilities
✅ **Scalability**: Classes directory can grow with subdomains
✅ **Testing Organization**: Tests are organized by type (unit/integration)
✅ **Consistency**: All infrastructure concerns in one place (utils)

## Import Path Reference

### Old → New

| Old Import | New Import |
|-----------|-----------|
| `from src.models.entities` | `from src.classes.models.entities` |
| `from src.models.schemas` | `from src.classes.models.schemas` |
| `from src.services.item_service` | `from src.classes.services.item_service` |
| `from src.repositories.item_repository` | `from src.classes.repositories.item_repository` |
| `from src.infrastructure.database` | `from src.utils.database` |
| `from src.infrastructure.cache` | `from src.utils.cache` |
| `from src.infrastructure.metrics` | `from src.utils.metrics` |

## Notes

- The old directories (`src/models/`, `src/services/`, `src/repositories/`, `src/infrastructure/`, `tests/`) should be **removed** after migration
- All import statements have been updated in the template files
- The `Makefile` has been updated to use `src/tests/` for pytest
- The `README.md` has been updated with the new structure diagram
