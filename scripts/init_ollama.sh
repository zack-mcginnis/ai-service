#!/bin/bash

echo "Waiting for Ollama to start..."
until $(curl --output /dev/null --silent --fail http://ollama:11434/api/version); do
    printf '.'
    sleep 1
done

echo "Pulling Deepseek model..."
curl -X POST http://ollama:11434/api/pull -d '{"name": "deepseek-coder:6.7b"}' 