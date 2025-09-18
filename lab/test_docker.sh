#!/bin/bash
# Docker Test Script

set -e

echo "🧪 Testing Docker Compose configuration..."

# Check if Docker is running
if ! docker info &> /dev/null; then
    echo "❌ Docker is not running"
    exit 1
fi

# Start services
echo "🚀 Starting Docker services..."
docker-compose -f docker/compose/basic.yml up -d

# Wait for services to be ready
echo "⏳ Waiting for services to be ready..."
sleep 10

# Test services
echo "🔍 Testing services..."

# Test web service
if curl -f http://localhost:8080 &> /dev/null; then
    echo "✅ Web service is responding"
else
    echo "❌ Web service test failed"
fi

# Test database
if docker-compose -f docker/compose/basic.yml exec -T database pg_isready -U testuser &> /dev/null; then
    echo "✅ Database is ready"
else
    echo "❌ Database test failed"
fi

# Test Redis
if docker-compose -f docker/compose/basic.yml exec -T redis redis-cli ping | grep -q PONG; then
    echo "✅ Redis is responding"
else
    echo "❌ Redis test failed"
fi

echo "📊 Service status:"
docker-compose -f docker/compose/basic.yml ps

# Cleanup
echo "🧹 Cleaning up..."
docker-compose -f docker/compose/basic.yml down

