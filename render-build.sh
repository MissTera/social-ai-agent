#!/bin/bash
set -o errexit

# Install system dependencies first
pip install --upgrade pip

# Install Python dependencies (avoid Rust compilation)
pip install fastapi==0.104.1
pip install uvicorn[standard]==0.24.0
pip install sqlalchemy==2.0.23
pip install python-dotenv==1.0.0
pip install requests==2.31.0
pip install pydantic==2.5.0

# Install cryptography with pre-compiled wheels (no Rust)
pip install cryptography==3.4.8 --no-binary=cryptography