"""
Module for Slack Alert functionality
Example usage:
    from utility import Slack
    slack = Slack.Alerts()
Created by: noahcalex@gmail.com
Initialized: April 8, 2022
"""

import requests
from datetime import datetime
import logging 


class Alerts:

    def __init__(self, send_to_slack: bool = True, environment='remote'):
        """_summary_
        Args:
            send_to_slack (bool, optional): Sends actual failure messages to slack channel. Set to False for testing purposes 
                as to not spam the failure channel. Defaults to True.
        """
        self.datetime_format = "%Y-%m-%dT%H:%M:%S"
        
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt=self.datetime_format)
        self.logger = logging.getLogger('Slack Alerts')
        
        self.send_to_slack = send_to_slack

        try:
            self.webhook_endpoint = ''
        except:
            self.logger.error("Failed to retrieve endpoint", exc_info=True)
            raise
        self.header = {
            'Content-type': 'application/json'
        }

    def send_slack_alert(self, severity: str, log_payload: str):
        cur_time = datetime.now().strftime(self.datetime_format)

        body = {
            "blocks": [
                    {
                        "type": "header",
                        "text": {
                            "type": "plain_text",
                            "text": "Backend Alert",
                            "emoji": True
                        }
                    },
                    {
                        "type": "section",
                        "fields": [
                            {
                                "type": "mrkdwn",
                                "text": f"*Severity:*\n {severity}"
                            }
                        ]
                    },
                    {
                        "type": "section",
                        "fields": [
                            {
                                "type": "mrkdwn",
                                "text": f"*When:*\n {cur_time}"
                            },
                            {
                                "type": "mrkdwn",
                                "text": f"*Log Payload:*\n {log_payload}"
                            }
                        ]
                    }
                ]
            }
        
        if self.send_to_slack:
            try:
                response = requests.post(self.webhook_endpoint, headers=self.header, json=body)
                return response
            except:
                self.logger.error("Failed Slack channel post", exc_info=True)
                return None
        else:
            return None
        
    def send_slack_success(self):
        cur_time = datetime.now().strftime(self.datetime_format)

        body = {
            "blocks": [
                    {
                        "type": "header",
                        "text": {
                            "type": "plain_text",
                            "text": "Cloud Function Success",
                            "emoji": True
                        }
                    },
                    {
                        "type": "section",
                        "fields": [
                            {
                                "type": "mrkdwn",
                                "text": f"*Function Name:*\n {self.cloud_function_id}"
                            },
                            {
                                "type": "mrkdwn",
                                "text": f"*When:*\n {cur_time}"
                            }
                        ]
                    }
                ]
            }
        
        if self.send_to_slack:
            try:
                response = requests.post(self.webhook_endpoint, headers=self.header, json=body)
                return response
            except:
                self.logger.error("Failed Slack channel post", exc_info=True)
                return None
        else:
            return None
        