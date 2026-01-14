#!/bin/bash
echo "=== Running Jakarta Roster Persistence Test ==="
echo "Container: $1"
echo

if [ -z "$1" ]; then
    echo "Usage: $0 <container_name_or_id>"
    echo "Example: $0 angry_newton"
    exit 1
fi

echo "Copying smoke test to container..."
docker cp smoke.py "$1":/smoke.py

echo "Running smoke test inside container..."
echo
docker exec "$1" python3 /smoke.py

echo
echo "=== Test Complete ==="
