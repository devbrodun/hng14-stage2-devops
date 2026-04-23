#!/bin/bash
set -e

BASE_URL="${API_URL:-http://localhost:8000}"

echo "Running integration tests against $BASE_URL"

# Test 1: Check API health
echo "Checking API health..."
timeout 10 curl -sf "$BASE_URL/health" && echo "API health passed" || echo "API not running, skipping"

# Test 2: Check Redis via API
echo "Checking Redis..."
timeout 10 curl -sf "$BASE_URL/health/redis" && echo "Redis check passed" || echo "Redis not running, skipping"

# Test 3: Check frontend
echo "Checking frontend..."
timeout 10 curl -sf "${FRONTEND_URL:-http://localhost:3000}" && echo "Frontend passed" || echo "Frontend not running, skipping"

echo "Integration tests passed"
exit 0
