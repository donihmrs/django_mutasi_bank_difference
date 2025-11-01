# Django Mutasi Selisih

A Django-based web application to compare bank mutation data with Zahir accounting exports, identify discrepancies (selisih), and generate summary reports.

The project includes a Dockerized setup, environment variable template, and Tailwind CSS.

## Features
- Upload and process bank mutation and Zahir spreadsheets (examples in `finance/private_file/`).
- Dashboard with quick overview.
- Views for:
  - Mutasi Bank
  - Mutasi Zahir
  - Laporan (report)
- Modular Django app structure (`finance` app).
- Containerized runtime using Docker and docker-compose.

## Project Structure
Key directories and files:
  - siteMutasi/ (Django project root)
    - settings.py, urls.py, wsgi.py, asgi.py
  - finance/ (Django app)
    - models.py, views.py, urls.py, admin.py, migrations/
    - private_file/ (example sample files)
  - templates/
    - app/ (base templates, navbar, dashboard, report pages)
  - static/
    - src/input.css (Tailwind input)
  - manage.py
  - requirements.txt
  - Dockerfile, docker-compose.yml
  - env.example

## Requirements
- Python 3.10+
- pip
- virtualenv (recommended)
- Alternatively: Docker and docker-compose

## Local Setup (without Docker)
1. Create and activate virtual environment:
   - Linux/macOS:
     ```bash
     python3 -m venv .venv
     source .venv/bin/activate
     ```
   - Windows (PowerShell):
     ```powershell
     py -3 -m venv .venv
     .venv\Scripts\Activate.ps1
     ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Environment variables:
   - Copy `env.example` to `.env` in the same folder and adjust values as needed.
4. Apply migrations:
   ```bash
   python manage.py migrate
   ```
5. Create superuser (optional but recommended):
   ```bash
   python manage.py createsuperuser
   ```
6. Run development server:
   ```bash
   python manage.py runserver
   ```
7. Open your browser at:
   - http://127.0.0.1:8000/

## Running with Docker
1. Ensure Docker and docker-compose are installed.
2. Copy environment file:
   - Copy `env.example` to `.env` and adjust values.
3. Build and start services:
   ```bash
   docker-compose up --build
   ```
4. Access the app at:
   - http://localhost:8000/

To stop containers:
```bash
docker-compose down
```

## Environment Variables
See `env.example` for configurable values. Typical variables:
- DJANGO_DEBUG=true|false
- DJANGO_SECRET_KEY=your-secret
- DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
- DATABASE_URL=sqlite:///db.sqlite3 (default) or a Postgres URL

If using Postgres via Docker, ensure `DATABASE_URL` matches docker-compose service.

## Static Files and Tailwind
- Source CSS: `static/src/input.css`
- You can integrate Tailwind build in your workflow (e.g., via Node or Django Tailwind). Currently, the repository provides the input file; adjust your pipeline as needed.

## Data Files
- Example spreadsheets are located in `finance/private_file/`:
  - `MUTASI_BANK.xlsx`
  - `ZAHIR.xlsx`
These are likely used by views in `finance/views.py` to parse and compare.

## Django Management
Common commands (run inside `root` directory):
- Apply migrations: `python manage.py migrate`
- Make migrations: `python manage.py makemigrations`
- Create superuser: `python manage.py createsuperuser`
- Run dev server: `python manage.py runserver`

## Testing
If/when tests are added in `finance/tests.py`:
```bash
python manage.py test
```

## Linting and Formatting
You can add and use tools like flake8, black, isort:
```bash
pip install black isort flake8
black .
isort .
flake8
```

## Deployment Notes
- Set `DJANGO_DEBUG=false` and configure `DJANGO_ALLOWED_HOSTS`.
- Use a strong `DJANGO_SECRET_KEY`.
- Configure a production-ready database (PostgreSQL recommended).
- Serve static files via WhiteNoise or a reverse proxy/CDN.
- Run behind a process manager (gunicorn/uvicorn) and reverse proxy (nginx).

## Troubleshooting
- If static files are not loading, ensure `STATIC_URL` and `STATICFILES_DIRS`/`STATIC_ROOT` are configured in `settings.py` and collectstatic is run for production.
- If migrations fail, delete the SQLite file (if using SQLite) and re-run migrations, or inspect migration history in `finance/migrations/`.
- For Docker issues, rebuild without cache: `docker-compose build --no-cache`.

## License
Specify your license here (e.g., MIT). Add a `LICENSE` file to the repository if applicable.

## Acknowledgements
- Django framework
- Tailwind CSS (if used in your build)
- Any libraries listed in `requirements.txt`
