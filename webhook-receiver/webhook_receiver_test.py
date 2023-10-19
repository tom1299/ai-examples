import unittest
import requests
import json


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

        response = requests.post("http://localhost:8000", data=json.dumps(event))

        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
