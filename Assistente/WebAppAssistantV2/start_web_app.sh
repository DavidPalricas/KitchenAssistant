#!/bin/bash

set -x
# This line sets the title of the terminal window (optional and may not work in all terminal emulators)
echo -ne "\033]0;Web App Assistant\007"

echo "Starting Web App Assistant..."
http-server -p 8082 -S -C cert.pem -K key.pem