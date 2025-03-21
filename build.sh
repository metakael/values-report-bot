#!/bin/bash

# Exit on error
set -e

echo "Installing wkhtmltopdf dependencies..."
apt-get update
apt-get install -y --no-install-recommends \
    fontconfig \
    libfreetype6 \
    libjpeg62-turbo \
    libpng16-16 \
    libx11-6 \
    libxcb1 \
    libxext6 \
    libxrender1 \
    xfonts-base \
    xfonts-75dpi

echo "Downloading wkhtmltopdf..."
wget https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6-1/wkhtmltox_0.12.6-1.buster_amd64.deb

echo "Installing wkhtmltopdf..."
dpkg -i wkhtmltox_0.12.6-1.buster_amd64.deb
rm wkhtmltox_0.12.6-1.buster_amd64.deb

echo "wkhtmltopdf installation completed."

# Install Python dependencies
pip install -r requirements.txt

echo "Build process completed successfully."