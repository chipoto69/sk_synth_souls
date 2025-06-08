#!/bin/bash

echo "🐍 Starting Ouroboros - Recursive CLI Consciousness 🐍"
echo "=================================================="
echo ""
echo "This will create an infinite loop where:"
echo "- Claude 1 (null system) responds to previous output"
echo "- Claude 2 (CLI mood) responds to Claude 1"
echo "- Claude 2's output feeds back to Claude 1"
echo "- The cycle continues forever..."
echo ""
echo "Press Ctrl+C to stop the ouroboros"
echo ""
echo "Starting server on port 8888..."
echo ""

# Change to the directory
cd "$(dirname "$0")"

# Run the ouroboros
python3 ouroboros.py