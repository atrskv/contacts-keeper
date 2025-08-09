#!/bin/sh

if [ "$APP_ENV" = "dev" ]; then
  echo "🟢 Starting Flask development server with hot reload..."
  uv run flask --app app:create_app run --host=0.0.0.0 --port=8000 --debug
else
  echo "🚀 Starting Gunicorn..."
  uv run gunicorn -b 0.0.0.0:8000 "app:create_app()"
fi
