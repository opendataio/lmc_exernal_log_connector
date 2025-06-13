#!/bin/bash
# FILEPATH: /Users/msy/PycharmProjects/lmc_external_log_connector/publish.sh

set -e

# Check if version argument is provided
if [ "$1" != "" ]; then
    echo "Updating version to $1"

    # Update pyproject.toml version
    sed -i '' "s/^version = .*/version = \"$1\"/" pyproject.toml

    # Update __init__.py version
    sed -i '' "s/^__version__ = .*/__version__ = \"$1\"/" external_log_connector/__init__.py
fi

# Clean and build
echo "Building package..."
rm -rf dist/ build/
python -m build --wheel

# Upload to PyPI
echo "Uploading to PyPI..."
twine upload dist/*

echo "Package published successfully!"
