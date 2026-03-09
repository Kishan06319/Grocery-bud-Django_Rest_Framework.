#!/usr/bin/env bash
set -o errexit

# Build React frontend
cd grocery-bud-react
npm install
npm run build
cd ..

# Install Python dependencies
pip install -r requirements.txt

# Collect static files and run migrations
python manage.py collectstatic --no-input
python manage.py migrate