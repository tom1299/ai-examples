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
# 4. The checksum is stored as a string in a transient list limited to 1000 if it is not yet contained in the list
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

# Load the Webex token from the file
WEBEX_SECRET_FILE = "/etc/webex-secret"
try:
    with open(WEBEX_SECRET_FILE, 'r') as f:
        webex_token = f.read().strip()
except FileNotFoundError:
    print("Webex secret file not found. Terminating.")
    exit(1)

# Initialize the list to store checksums
checksums = set()

# Webex room ID
WEBEX_ROOM_ID = os.getenv("WEBEX_ROOM_ID")

# Create a logger
logging.basicConfig(level=logging.INFO)

class WebhookHandler(http.server.BaseHTTPRequestHandler):
    def _calculate_checksum(self, event):
        fields_to_hash = [
            event['involvedObject']['uid'],
            event['metadata']['toolkit.fluxcd.io/revision'],
            event['severity'],
            event['message'],
            event['reason'],
        ]
        event_data = ''.join(fields_to_hash)
        checksum = hashlib.sha256(event_data.encode()).hexdigest()
        return checksum

    def _send_to_webex(self, event, checksum):
        if checksum not in checksums:
            checksums.add(checksum)
            payload = {
                "roomId": WEBEX_ROOM_ID,
                "text": json.dumps(event, indent=4)
            }
            headers = {
                "Authorization": f"Bearer {webex_token}",
                "Content-Type": "application/json"
            }
            response = requests.post("https://webexapis.com/v1/messages", headers=headers, json=payload)
            if response.status_code == 200:
                logging.info(f"Event sent to Webex: {checksum}")
            else:
                logging.error(f"Failed to send event to Webex: {checksum}")

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        event = json.loads(post_data)
        
        # 1. Log the event
        logging.info(f"Received event: {event}")

        # 2. Calculate the checksum
        checksum = self._calculate_checksum(event)
        logging.info(f"Calculated checksum: {checksum}")

        # 3. Check if checksum is in the list
        if checksum in checksums:
            logging.info(f"Checksum is already in the list: {checksum}")
        else:
            # 4. Store checksum in the list
            self._send_to_webex(event, checksum)
            # 5. Log whether the checksum is already in the list
            logging.info(f"Checksum added to the list: {checksum}")

def run_server():
    server_address = ('', 8000)
    httpd = http.server.HTTPServer(server_address, WebhookHandler)
    logging.info("Webhook receiver is running on port 8000.")
    httpd.serve_forever()

if __name__ == '__main__':
    run_server()
