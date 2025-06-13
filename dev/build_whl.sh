#!/bin/bash
# Clean old build artifacts
rm -rf dist/ build/

# Generate whl package (using pep517 standard)
python -m build --wheel

echo "Build completed, whl file is located in dist/ directory"
