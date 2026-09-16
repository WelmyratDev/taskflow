#!/bin/bash

# Directory for migrations
MIGRATIONS_DIR="migrations"

# Check if an argument is provided
if [ -z "$1" ]; then
  echo "Usage: $0 <migration_name>"
  exit 1
fi

# Migration name (first argument)
NAME="$1"

# Create directory if it doesn't exist
if [ ! -d "$MIGRATIONS_DIR" ]; then
  mkdir -p "$MIGRATIONS_DIR"
  echo "Created directory $MIGRATIONS_DIR"
fi

# Timestamp
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")

# File name
FILENAME="${MIGRATIONS_DIR}/${TIMESTAMP}_${NAME}.sql"

# Create empty file
touch "$FILENAME"

echo "Created migration file: $FILENAME"