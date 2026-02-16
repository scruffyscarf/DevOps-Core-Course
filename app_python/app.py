"""
DevOps Info Service
Main application module
"""
import os
import platform
import socket
import time
import logging
import json
from datetime import datetime, timezone
from flask import Flask, jsonify, request
from pythonjsonlogger import jsonlogger

# Configuration
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", 5000))
DEBUG = os.getenv("DEBUG", "False").lower() == "true"
APP_NAME = os.getenv("APP_NAME", "devops-info-service")

# Application start time
app = Flask(__name__)
start_time = time.time()

# JSON Logging setup
class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super(CustomJsonFormatter, self).add_fields(log_record, record, message_dict)
        log_record['timestamp'] = datetime.utcnow().isoformat()
        log_record['app'] = APP_NAME
        log_record['level'] = record.levelname
        log_record['module'] = record.module
        log_record['function'] = record.funcName
        log_record['line'] = record.lineno

# Configure root logger
log_handler = logging.StreamHandler()
formatter = CustomJsonFormatter('%(timestamp)s %(level)s %(name)s %(message)s')
log_handler.setFormatter(formatter)

# Remove existing handlers and add our JSON handler
logging.getLogger().handlers = []
logging.getLogger().addHandler(log_handler)
logging.getLogger().setLevel(logging.INFO)

# Also configure Flask logger
for handler in app.logger.handlers:
    app.logger.removeHandler(handler)
app.logger.addHandler(log_handler)
app.logger.setLevel(logging.INFO)

# Helpers
def get_uptime():
    uptime_seconds = int(time.time() - start_time)
    hours = uptime_seconds // 3600
    minutes = (uptime_seconds % 3600) // 60
    return uptime_seconds, f"{hours} hour(s), {minutes} minute(s)"

# Request logging decorators
@app.before_request
def log_request_info():
    """Log details before processing request"""
    app.logger.info("Request started", extra={
        'http_method': request.method,
        'path': request.path,
        'client_ip': request.remote_addr,
        'user_agent': request.headers.get('User-Agent', 'unknown'),
        'content_type': request.content_type
    })

@app.after_request
def log_response_info(response):
    """Log details after processing request"""
    app.logger.info("Request completed", extra={
        'http_method': request.method,
        'path': request.path,
        'status_code': response.status_code,
        'content_length': response.content_length,
        'mimetype': response.mimetype
    })
    return response

# Routes
@app.route("/", methods=["GET"])
def main_info():
    """Main endpoint - service and system information."""
    try:
        uptime_seconds, uptime_human = get_uptime()

        response = {
            "service": {
                "name": APP_NAME,
                "version": "1.0.0",
                "description": "DevOps course info service",
                "framework": "Flask"
            },
            "system": {
                "hostname": socket.gethostname(),
                "platform": platform.system(),
                "platform_version": platform.version(),
                "architecture": platform.machine(),
                "cpu_count": os.cpu_count(),
                "python_version": platform.python_version()
            },
            "runtime": {
                "uptime_seconds": uptime_seconds,
                "uptime_human": uptime_human,
                "current_time": datetime.now(timezone.utc).isoformat(),
                "timezone": "UTC"
            },
            "request": {
                "client_ip": request.remote_addr,
                "user_agent": request.headers.get("User-Agent"),
                "method": request.method,
                "path": request.path
            },
            "endpoints": [
                {"path": "/", "method": "GET", "description": "Service information"},
                {"path": "/health", "method": "GET", "description": "Health check"}
            ]
        }

        app.logger.info("Main endpoint processed successfully", extra={
            'endpoint': 'main_info',
            'client_ip': request.remote_addr,
            'response_size': len(jsonify(response).get_data())
        })
        return jsonify(response)
    
    except Exception as e:
        app.logger.error("Error in main endpoint", extra={
            'endpoint': 'main_info',
            'error': str(e),
            'error_type': type(e).__name__
        })
        return jsonify({"error": "Internal server error"}), 500


@app.route("/health", methods=["GET"])
def health_check():
    """Health endpoint - available server information."""
    uptime_seconds, _ = get_uptime()

    response = {
        "status": "healthy",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "uptime_seconds": uptime_seconds
    }

    app.logger.info("Health check processed", extra={
        'endpoint': 'health_check',
        'status': 'healthy',
        'uptime_seconds': uptime_seconds
    })
    return jsonify(response), 200


@app.errorhandler(404)
def not_found(error):
    app.logger.warning("404 Not Found", extra={
        'path': request.path,
        'method': request.method,
        'client_ip': request.remote_addr
    })
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(500)
def internal_error(error):
    app.logger.error("500 Internal Server Error", extra={
        'path': request.path,
        'method': request.method,
        'error': str(error)
    })
    return jsonify({"error": "Internal server error"}), 500

# Run
if __name__ == "__main__":
    app.logger.info("Starting application", extra={
        'host': HOST,
        'port': PORT,
        'debug': DEBUG,
        'app_name': APP_NAME
    })
    app.run(host=HOST, port=PORT, debug=DEBUG)
