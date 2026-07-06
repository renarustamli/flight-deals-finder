"""
Notification Manager.

Handles sending flight deal notifications using the Twilio API.
Supports both SMS and WhatsApp messaging.
"""

import os

from twilio.rest import Client


class NotificationManager:
    """Send notifications through Twilio."""

    def __init__(self) -> None:
        """Initialize the Twilio client using environment variables."""
        self.client = Client(
            os.environ["TWILIO_SID"],
            os.environ["TWILIO_AUTH_TOKEN"],
        )

    def send_sms(self, message_body: str) -> None:
        """
        Send a flight deal notification via SMS.

        Args:
            message_body: The notification message to send.
        """
        message = self.client.messages.create(
            from_=os.environ["TWILIO_VIRTUAL_NUMBER"],
            to=os.environ["TWILIO_VERIFIED_NUMBER"],
            body=message_body,
        )

        print(f"SMS sent successfully (SID: {message.sid})")

    def send_whatsapp(self, message_body: str) -> None:
        """
        Send a flight deal notification via WhatsApp.

        Note:
            This method requires the Twilio WhatsApp Sandbox or an
            approved WhatsApp Business sender.

        Args:
            message_body: The notification message to send.
        """
        message = self.client.messages.create(
            from_=f'whatsapp:{os.environ["TWILIO_WHATSAPP_NUMBER"]}',
            to=f'whatsapp:{os.environ["TWILIO_VERIFIED_NUMBER"]}',
            body=message_body,
        )

        print(f"WhatsApp message sent successfully (SID: {message.sid})")

