#!/bin/bash

# Install MariaDB using Homebrew
echo "Installing MariaDB..."
brew install mariadb

# Start MariaDB Server
echo "Starting MariaDB server..."
brew services start mariadb
