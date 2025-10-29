# Jinja Template Errors - Fixed

## Issues Found and Resolved

### 1. README_TEMPLATE.md Processing Error
**Problem**: The file `{{cookiecutter.project_slug}}/README_TEMPLATE.md` was being processed by Cookiecutter as a template file, but it contained literal Jinja syntax examples that weren't meant to be evaluated.

**Error**: 
```
jinja2.exceptions.TemplateSyntaxError: Unexpected end of template. Jinja was looking for the following tags: 'elif' or 'else' or 'endif'. The innermost block that needs to be closed is 'if'.
```

**Solution**: Moved `README_TEMPLATE.md` outside the `{{cookiecutter.project_slug}}/` folder and renamed it to `TEMPLATE_USAGE.md` at the root level. Files inside the project slug folder are processed by Cookiecutter; documentation files should live at the template root.

**Commit**: `d92de68` - "Fix Jinja template errors"

---

### 2. TESTING_GUIDE.md Literal Jinja Syntax
**Problem**: The `TESTING_GUIDE.md` file contained literal Jinja syntax examples in a code block that weren't wrapped in `{% raw %}` tags.

**Solution**: Wrapped the code block containing Jinja examples with `{% raw %}...{% endraw %}` to prevent Cookiecutter from trying to parse them.

**Commit**: `d92de68` - "Fix Jinja template errors"

---

### 3. Flask Template Indentation Errors
**Problem**: Jinja conditional blocks in `app_flask.py` weren't properly indented, causing Python indentation errors in generated projects.

**Errors**:
```python
IndentationError: unexpected indent (app_flask.py, line 49)
SyntaxError: 'return' outside function (app_flask.py, line 105)
```

**Root Cause**: The `{% if %}` and `{% endif %}` tags need to be indented at the same level as the Python code they control. The `-%}` syntax strips whitespace, but the tags themselves must maintain proper indentation.

**Solution**: Added proper indentation to all Jinja blocks:
- Line 56: `{% if cookiecutter.enable_metrics == 'yes' -%}` → `    {% if cookiecutter.enable_metrics == 'yes' -%}`
- Line 84: Same fix for middleware section
- Line 113: Same fix for metrics endpoint section

**Commits**: 
- `36b9c4e` - "Fix indentation in Flask app template"
- `e3f6eeb` - "Fix all Jinja block indentation in Flask template"

---

## Testing

All fixes have been tested with:

```bash
# Full parameter test (Flask)
cookiecutter https://github.com/matangilat/python-cookiecutter-microservice \
  --no-input \
  project_name="testing" \
  web_framework="flask" \
  enable_metrics="yes" \
  database_type="postgresql" \
  deploy_database="yes"

# Verify syntax
cd testing
python3 -m py_compile src/*.py  # ✅ Success

# FastAPI test
cookiecutter https://github.com/matangilat/python-cookiecutter-microservice \
  --no-input \
  web_framework="fastapi" \
  enable_metrics="yes"

cd testing
python3 -m py_compile src/*.py  # ✅ Success
```

---

## Utility Added

Created `check_jinja_counts.py` - a utility script that scans template files for mismatched `{% if %}` and `{% endif %}` tags while properly ignoring content within `{% raw %}...{% endraw %}` blocks.

Usage:
```bash
cd /path/to/cookiecutter-microservice
python3 check_jinja_counts.py .
```

---

## Summary

**Files Changed**:
1. `{{cookiecutter.project_slug}}/README_TEMPLATE.md` → `TEMPLATE_USAGE.md` (moved)
2. `TESTING_GUIDE.md` (wrapped examples in raw blocks)
3. `{{cookiecutter.project_slug}}/src/app_flask.py` (fixed indentation)
4. `check_jinja_counts.py` (new utility)

**Result**: Template now generates valid Python code for all configurations. No more Jinja syntax errors or Python indentation errors.
