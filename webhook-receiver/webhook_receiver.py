# You are an expert python programmer.
# Task: Implement the following specification:
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
# - The Token used for authenticating against webex is read from the file "/var/tmp/webex-secret once at the start of the program. If the secret is not found, the program will terminate with
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

# Contains the <name><namespace><kind> ad key and the <severity> as a value
states = {}

# Webex room ID
WEBEX_ROOM_ID = os.getenv("WEBEX_ROOM_ID")
if WEBEX_ROOM_ID is None:
    print("WEBEX_ROOM_ID environment variable is not set. Terminating.")
    exit(1)
    

# Create a logger
logging.basicConfig(level=logging.INFO)


class WebhookHandler(http.server.BaseHTTPRequestHandler):

    def get_unique_id(self, event):
        fields_to_hash = [
            event['involvedObject']['kind'],
            event['involvedObject']['name'],
            event['involvedObject']['namespace']
        ]
        event_data = ''.join(fields_to_hash)
        unique_key = hashlib.sha256(event_data.encode()).hexdigest()
        return unique_key

    def create_markdown(self, event):
        emoji = "\u2705"
        if event['severity'] == "error":
            emoji = "\u274C"

        markdown = f"{emoji} **{event['involvedObject']['kind'].lower()}/{event['involvedObject']['name']}.{event['involvedObject']['namespace']}**\n"
        markdown += f"{event['message']}\n"

        if event['metadata']:
            for k, v in event['metadata'].items():
                markdown += f">**{k}**: {v}\n"

        return markdown

    def _send_to_webex(self, event, object_id):
        payload = {
            "roomId": WEBEX_ROOM_ID,
            "markdown": self.create_markdown(event)
        }
        headers = {
            "Authorization": f"Bearer {webex_token}",
            "Content-Type": "application/json"
        }
        response = requests.post("https://webexapis.com/v1/messages", headers=headers, json=payload)
        if response.status_code == 200:
            logging.info(f"Event sent to Webex: {object_id}")
        else:
            logging.error(f"Failed to send event to Webex: {object_id}")

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        event = json.loads(post_data)
        
        # 1. Log the event
        logging.info(f"Received event: {event}")

        # 2. Get the id of the involved object
        unique_id = self.get_unique_id(event)

        logging.info(f"Event is for object: {unique_id}")

        # 3. Get the current state of the object
        current_state = states.get(unique_id)

        # 4. Check the current state of the object and sent it to Webex if it has changed
        if current_state is None or current_state != event['severity']:
            logging.info(f"State changed from {current_state} to {event['severity']}")
            self._send_to_webex(event, unique_id)
            states[unique_id] = event['severity']
        else:
            logging.info(f"State unchanged: {current_state} for object {unique_id}")

        self.send_response(200)
        self.end_headers()

def run_server():
    server_address = ('', 8000)
    httpd = http.server.HTTPServer(server_address, WebhookHandler)
    logging.info("Webhook receiver is running on port 8000.")
    httpd.serve_forever()

if __name__ == '__main__':
    run_server()
