import unittest
import http.server
import requests
import threading
import time
import json
import hashlib
import os

from webhook_receiver import WebhookHandler

class TestWebhookReceiver(unittest.TestCase):

    def test_webhook_processing(self):
        # Define a sample event payload
        event = {
            "involvedObject": {
                "kind": "HelmRelease",
                "name": "sample-app",
                "namespace": "default",
                "uid": "12345",
            },
            "metadata": {
                "toolkit.fluxcd.io/revision": "v1",
            },
            "severity": "error",
            "message": "Sample message",
            "reason": "Sample reason",
        }

        # Calculate the checksum for ^ event
        fields_to_hash = [
            event['involvedObject']['uid'],
            event['metadata']['toolkit.fluxcd.io/revision'],
            event['severity'],
            event['message'],
            event['reason'],
        ]
        event_data = ''.join(fields_to_hash)

        # Send the event to the webhook receiver
        response = requests.post("http://localhost:8000", data=json.dumps(event))

        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
