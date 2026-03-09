#!/usr/bin/env bash
set -o errexit

echo "Building React frontend..."
cd grocery-bud-react
npm install
npm run build

# Verify dist directory was created
if [ ! -d "dist" ]; then
    echo "ERROR: dist directory not created!"
    exit 1
fi

echo "React build complete"
cd ..

echo "Installing Python dependencies..."
pip install -r requirements.txt

echo "Collecting static files..."
python manage.py collectstatic --no-input

echo "Running migrations..."
python manage.py migrate

echo "Build complete!"