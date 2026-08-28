"""
DevOps Dashboard - a small Flask app used as the base project for a
full DevOps lifecycle demo (Git -> Docker -> Jenkins -> Ansible -> Cloud -> Monitoring).

The app itself is intentionally simple. Its job is to give us something
real to build, containerize, deploy, and monitor - not to show off Python.
"""

import os
import platform
import socket
from datetime import datetime, timezone

from flask import Flask, jsonify, render_template

app = Flask(__name__)

# Version is read from an env var so later, when we add Docker/CI/CD,
# we can bump this on every build without touching code (e.g. git commit hash).
APP_VERSION = os.environ.get("APP_VERSION", "0.2.0")
ENVIRONMENT = os.environ.get("APP_ENV", "development")


def get_system_info():
    """Collect basic host info to display on the dashboard."""
    return {
        "hostname": socket.gethostname(),
        "platform": platform.system(),
        "platform_version": platform.release(),
        "python_version": platform.python_version(),
    }


@app.route("/")
def dashboard():
    """Human-facing dashboard page."""
    context = {
        "status": "UP",
        "version": APP_VERSION,
        "environment": ENVIRONMENT,
        "system_info": get_system_info(),
        "server_time": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC"),
    }
    return render_template("index.html", **context)


@app.route("/health")
def health():
    """
    Machine-facing health check endpoint.
    This is the endpoint Docker/Jenkins/monitoring tools will actually poll -
    it's standard practice to separate this from the human dashboard page.
    """
    return jsonify(status="healthy", version=APP_VERSION), 200


@app.route("/api/info")
def api_info():
    """JSON version of the dashboard data - useful for testing and for Prometheus later."""
    return jsonify(
        status="UP",
        version=APP_VERSION,
        environment=ENVIRONMENT,
        system_info=get_system_info(),
    )


if __name__ == "__main__":
    # host=0.0.0.0 matters later: inside a Docker container, 127.0.0.1
    # would only be reachable from inside the container itself.
    app.run(host="0.0.0.0", port=5000, debug=(ENVIRONMENT == "development"))
