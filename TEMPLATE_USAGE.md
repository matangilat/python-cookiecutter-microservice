This directory contains a Cookiecutter template for a Flask microservice.

Important: Do NOT run the Python files inside this template directory directly. They contain Jinja/Cookiecutter template tags (for example, the template expression below) which are not valid Python until the template is rendered by Cookiecutter:

{% raw %}
`{% if cookiecutter.enable_metrics %}` and `{{ cookiecutter.project_slug }}`
{% endraw %}

How to use this template

1. Install Cookiecutter if you don't have it:

   pip install cookiecutter

2. Generate a project from this template. From the repo root or from a parent folder run:

   cookiecutter ./cookiecutter-microservice

   Cookiecutter will prompt for the template variables (project slug, whether to enable metrics, etc.). It will create a new folder with the rendered project files.

3. Run the generated project

   - cd into the newly generated project folder (the name you chose for `project_slug`).
   - (Recommended) create and activate a virtualenv, then install requirements:

     python3 -m venv .venv
     source .venv/bin/activate
     pip install -r requirements.txt

   - Start the app (example):

     python -m src.app_flask

Notes and tips

- If you want to produce an example rendered project without interactive prompts, use the `--no-input` and `extra_context` features of Cookiecutter (see Cookiecutter docs).

- If you need to test the template inside a container/image, first render the template inside the image (e.g., run `cookiecutter` there) and then run the generated project's code. Running the template files directly inside the image will cause SyntaxError/IndentationError because of raw Jinja tags.

- If you'd like, I can add a convenience script that programmatically renders the template into `./examples/<name>` (non-interactive) and optionally runs a quick smoke test. Ask and I'll add it.
