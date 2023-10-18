You are an expert python programmer.
Task: Implement the following specification:
# Context: A web hook receiver based on the http.server module
# that will receive a POST request from a webhook containing
# events in flux notification event format. The process is as follows:
# 1. The event is logged
# 2. A checksum of the event is calculated based on the following fields:
#   - involvedObject.uid
#   - metadata.toolkit.fluxcd.io/revision
#   - severity
#   - message
#   - reason
# 3. The checksum is logged
# 4. The checksum is stored as a string in a list limited to 1000 if it is not yet contained in the list
# 5. Log whether the checksum is already in the list
# 6. If the checksum is not yet stored in the list, the the event is sent to a webex channel identified by the WEBEX_ROOM_ID environment variable
# Additional information:
# - The Token used for authenticating against webex is read from the file "/etc/webex-secret once at the start of the program. If the secret is not found, the program will terminate with
# an appropriate error message
# - Logging is done using pythons logging library in the following json format {<time_stamp>, <log_level>, <message>}

import http.server
import json
import hashlib
import logging
import os
import requests

# Define the path to store the checksums
CHECKSUMS_FILE = "checksums.txt"

# Configure the logging format
logging.basicConfig(level=logging.INFO, format='{"time_stamp": "%(asctime)s", "log_level": "%(levelname)s", "message": "%(message)s"}')

# Function to read the Webex secret from a file
def get_webex_secret():
    try:
        with open("/etc/webex-secret", "r") as secret_file:
            return secret_file.read().strip()
    except FileNotFoundError:
        logging.error("Webex secret file not found. Program terminated.")
        exit(1)

# Function to send an event to Webex
def send_event_to_webex(event, webex_token, webex_room_id):
    headers = {
        'Authorization': f'Bearer {webex_token}',
        'Content-Type': 'application/json'
    }
    data = {
        'roomId': webex_room_id,
        'text': json.dumps(event, indent=4)
    }

    response = requests.post('https://webexapis.com/v1/messages', headers=headers, json=data)

    if response.status_code == 200:
        logging.info("Event sent to Webex successfully.")
    else:
        logging.error(f"Failed to send event to Webex. Status Code: {response.status_code}")
        logging.error(response.text)

# Function to calculate the checksum
def calculate_checksum(event):
    fields = [
        event.get('involvedObject', {}).get('uid', ''),
        event.get('metadata', {}).get('toolkit.fluxcd.io/revision', ''),
        event.get('severity', ''),
        event.get('message', ''),
        event.get('reason', '')
    ]

    checksum = hashlib.sha256(json.dumps(fields).encode()).hexdigest()
    return checksum

# Function to load existing checksums from file
def load_checksums():
    checksums = set()
    if os.path.exists(CHECKSUMS_FILE):
        with open(CHECKSUMS_FILE, "r") as file:
            for line in file:
                checksums.add(line.strip())
    return checksums

# Function to save the checksums to file
def save_checksums(checksums):
    with open(CHECKSUMS_FILE, "w") as file:
        for checksum in checksums:
            file.write(checksum + "\n")

# Main request handler
class WebhookHandler(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        event = json.loads(post_data)

        logging.info("Received event:")
        logging.info(json.dumps(event, indent=4))

        checksum = calculate_checksum(event)
        logging.info("Checksum: " + checksum)

        checksums = load_checksums()
        if checksum in checksums:
            logging.info("Checksum already in the list.")
        else:
            logging.info("Checksum not in the list. Storing it.")
            checksums.add(checksum)
            if len(checksums) > 1000:
                # Remove the oldest checksums if the list exceeds 1000 items
                checksums = list(checksums)[-1000:]
            save_checksums(checksums)
            webex_token = get_webex_secret()
            webex_room_id = os.environ.get("WEBEX_ROOM_ID")
            send_event_to_webex(event, webex_token, webex_room_id)

        self.send_response(200)
        self.end_headers()

if __name__ == '__main__':
    # Ensure the directory exists for the checksums file
    os.makedirs(os.path.dirname(CHECKSUMS_FILE), exist_ok=True)

    try:
        server_address = ('', 8080)
        httpd = http.server.HTTPServer(server_address, WebhookHandler)
        logging.info("Webhook receiver is running on port 8080.")
        httpd.serve_forever()
    except KeyboardInterrupt:
        logging.info("Webhook receiver terminated.")
