#!/usr/bin/env bash
set -o errexit

echo "=== Starting build process ==="

# Build React frontend
echo "Building React frontend..."
cd grocery-bud-react
npm install
npm run build

# Verify dist directory was created
if [ ! -d "dist" ]; then
    echo "ERROR: dist directory not created!"
    exit 1
fi

echo "React build complete - dist directory exists"
ls -la dist/
cd ..

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --no-input --verbosity=2

# Run migrations
echo "Running migrations..."
python manage.py migrate --verbosity=2

# Verify the setup
echo "Verifying setup..."
python manage.py check --deploy

echo "=== Build complete! ==="