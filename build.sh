#!/bin/bash

# Replace this with your actual GitHub repo name
REPO_NAME="static_site_generator"

echo "Building site with base path /$REPO_NAME/"

python3 src/main.py "/$REPO_NAME/"
