FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project files
COPY . .

# Collect static files
RUN python interior_planner/manage.py collectstatic --noinput

# Cloud Run expects the app to listen on port 8080
EXPOSE 8080

CMD ["gunicorn", "interior_planner.interior_planner.wsgi:application", "--bind", "0.0.0.0:8080"]