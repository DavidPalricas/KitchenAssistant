#!/bin/bash

# Install MariaDB using Homebrew
echo "Installing MariaDB..."
brew install mariadb

# Install mysql-connector-python
echo "Installing mysql-connector-python..."
brew install mysql-connector-python

# Start MariaDB Server
echo "Starting MariaDB server..."
brew services start mariadb

