from flask import Flask, request, jsonify
import json
import time
import hashlib
import os

app = Flask(__name__)

LICENSE_FILE = "license_data.json"

DEFAULT_LICENSE = {
    "key": "BETA2025",
    "start_time": 1716508800,
    "duration_days": 3,
    "max_users": 5,
    "allowed_devices": []
}

def load_license():
    if not os.path.exists(LICENSE_FILE):
        with open(LICENSE_FILE, "w") as f:
            json.dump(DEFAULT_LICENSE, f, indent=2)
    with open(LICENSE_FILE, "r") as f:
        return json.load(f)

def save_license(data):
    with open(LICENSE_FILE, "w") as f:
        json.dump(data, f, indent=2)

@app.route("/check_license", methods=["POST"])
def check_license():
    data = request.json
    device_id = data.get("device_id")
    key = data.get("key")
    now = int(data.get("timestamp", time.time()))

    license_data = load_license()
    expiry_time = license_data["start_time"] + license_data["duration_days"] * 86400

    if key != license_data["key"]:
        return jsonify({"status": "invalid_key"}), 401
    if now > expiry_time:
        return jsonify({"status": "expired"}), 403
    if device_id in license_data["allowed_devices"]:
        return jsonify({"status": "valid"})
    if len(license_data["allowed_devices"]) < license_data["max_users"]:
        license_data["allowed_devices"].append(device_id)
        save_license(license_data)
        return jsonify({"status": "registered"})
    return jsonify({"status": "full"}), 403

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
