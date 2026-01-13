#!/bin/bash

echo "🚀 Starting Railway deployment..."

# Run database migrations
echo "📊 Running database migrations..."
python manage.py migrate

# Create sample users
echo "👥 Creating sample users..."
python create_sample_users.py

# Start the Django server
echo "🌐 Starting Django server..."
python manage.py runserver 0.0.0.0:$PORT