import requests
import sys

EC2_URL = "http://44.200.228.146/"
TIMEOUT = 5

print("=== Health Check Start ===")

try:
    response = requests.get(EC2_URL, timeout=TIMEOUT)
    status_code = response.status_code

    print(f"HTTP Status: {status_code}")

    if status_code == 200:
        print("Health check PASSED")
        sys.exit(0)
    else:
        print("Health check FAILED")
        sys.exit(1)

except Exception as e:
    print("Health check ERROR")
    print(str(e))
    sys.exit(1)
