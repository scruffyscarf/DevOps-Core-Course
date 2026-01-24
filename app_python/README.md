# DevOps Info Service

## Overview
A simple Python web service that provides system and runtime information.

## Prerequisites
- Python 3.11+
- Flask==3.1.0

## Installation
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Running the Application
```bash
python app.py
# Or with custom config
PORT=8080 python app.py
```

## API Endpoints
- **GET /** - Service and system information
- **GET /health** - Health check