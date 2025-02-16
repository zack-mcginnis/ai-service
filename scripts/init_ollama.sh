#!/bin/bash

echo "Waiting for Ollama to start..."
until $(curl --output /dev/null --silent --fail http://ollama:11434/api/version); do
    printf '.'
    sleep 1
done

echo "Pulling Deepseek model..."
curl -X POST http://ollama:11434/api/pull \
     -H 'Content-Type: application/json' \
     -d '{"model": "deepseek-r1:1.5b"}' \
     -v

# Wait for model to be ready
echo "Waiting for model to be ready..."
until curl -s http://ollama:11434/api/tags | grep -q "deepseek-r1:1.5b"; do
    printf '.'
    sleep 5
done

echo "Model is ready!"

# Verify model
curl -s http://ollama:11434/api/tags | grep "deepseek-r1" 