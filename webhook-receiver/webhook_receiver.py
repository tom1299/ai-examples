import hashlib
import http.server
import json
import logging
import os
import sys

import requests


class JsonFormatter(logging.Formatter):

    def format(self, record):
        if isinstance(record.msg, dict):
            message = record.msg
        else:
            message = record.getMessage()
        log_record = {'timestamp': self.formatTime(record), 'level': record.levelname, 'message': message, }
        return json.dumps(log_record)


logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = JsonFormatter()
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

logger = logging.getLogger(__name__)

WEBEX_SECRET_FILE = "/etc/webex-secret"

try:
    with open(WEBEX_SECRET_FILE, 'r', encoding="utf-8") as f:
        webex_token = f.read().strip()
except FileNotFoundError:
    logger.warning("Webex secret file %s not found. "
                   "Trying to read from environment variable WEBEX_TOKEN", WEBEX_SECRET_FILE)
    webex_token = os.getenv("WEBEX_TOKEN")
    if webex_token is None:
        logger.error("Neither secret file %s nor environment variable WEBEX_TOKEN found. "
                     "Can not authenticate against Webex", WEBEX_SECRET_FILE)
        sys.exit(1)

WEBEX_ROOM_ID = os.getenv("WEBEX_ROOM_ID")
if WEBEX_ROOM_ID is None:
    print("WEBEX_ROOM_ID environment variable is not set")
    sys.exit(1)


class WebhookHandler(http.server.BaseHTTPRequestHandler):

    __states = {}

    # noinspection PyMethodMayBeStatic
    def __get_unique_id(self, event):
        fields_to_hash = [event['involvedObject']['kind'], event['involvedObject']['name'],
                          event['involvedObject']['namespace']]
        event_data = ''.join(fields_to_hash)
        unique_key = hashlib.sha256(event_data.encode()).hexdigest()
        return unique_key

    # noinspection PyMethodMayBeStatic
    def __create_markdown(self, event):
        emoji = "\u2705"
        if event['severity'] == "error":
            emoji = "\u274C"

        markdown = (f"{emoji} **{event['involvedObject']['kind'].lower()}/{event['involvedObject']['name']}"
                    f".{event['involvedObject']['namespace']}**\n")
        markdown += f"{event['message']}\n"

        if event['metadata']:
            for key, value in event['metadata'].items():
                markdown += f">**{key}**: {value}\n"

        return markdown

    def __send_to_webex(self, event, object_id):
        payload = {"roomId": WEBEX_ROOM_ID, "markdown": self.__create_markdown(event)}
        headers = {"Authorization": f"Bearer {webex_token}", "Content-Type": "application/json"}
        response = requests.post("https://webexapis.com/v1/messages", headers=headers, json=payload, timeout=5)
        if response.status_code == 200:
            logging.info("Event sent to Webex: %s", object_id)
        else:
            logging.error("Failed to send event to Webex: %s", object_id)

    # noinspection PyPep8Naming, invalid-name
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        event = json.loads(post_data)

        logging.info("Received event: %s", event)

        unique_id = self.__get_unique_id(event)

        logging.info("Event is for object: %s", unique_id)

        current_state = self.__states.get(unique_id)

        if current_state is None or current_state != event['severity']:
            logging.info("State changed from %s to %s", current_state, event['severity'])
            self.__send_to_webex(event, unique_id)
            self.__states[unique_id] = event['severity']
        else:
            logging.info("State unchanged: %s for object %s", current_state, unique_id)

        self.send_response(200)
        self.end_headers()


def run_server():
    server_address = ('', 8000)
    httpd = http.server.HTTPServer(server_address, WebhookHandler)
    logging.info("Webhook receiver is running on port 8000")
    httpd.serve_forever()


if __name__ == '__main__':
    run_server()
