import requests
import hashlib
import getpass
import time
import os
import sys

LICENSE_API_URL = "https://license-api-dsxu.onrender.com"  # Replace with real URL
SHARED_LICENSE_KEY = "BETA2025"  # Public info – no secrets

# --- ANTI DEBUG ---
def anti_debug():
    if sys.gettrace():
        print("🚨 Debugger detected. Exiting.")
        os._exit(1)

# --- DEVICE FINGERPRINT ---
def get_device_id():
    username = getpass.getuser()
    return hashlib.sha256(username.encode()).hexdigest()

# --- LICENSE CHECK ---
def check_license():
    anti_debug()  # Kill if debugger present

    device_id = get_device_id()
    now = int(time.time())

    try:
        response = requests.post(LICENSE_API_URL, json={
            "device_id": device_id,
            "key": SHARED_LICENSE_KEY,
            "timestamp": now
        }, timeout=5)

        if response.status_code == 200:
            result = response.json()["status"]
            if result in ["valid", "registered"]:
                print("✅ License verified.")
                return True
            else:
                print(f"❌ Access denied: {result}")
        else:
            print(f"❌ Server error: {response.status_code}")

    except Exception as e:
        print(f"❌ License check failed: {e}")

    os._exit(1)  # Hard kill on failure
    return False
