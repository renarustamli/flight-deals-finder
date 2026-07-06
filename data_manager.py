"""
Data Manager.

Handles communication with the Google Sheets database through the
Sheety API. This module is responsible for retrieving destination
data and updating the stored lowest flight prices.
"""

import os

import requests
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth

load_dotenv()

SHEETY_ENDPOINT = (
    "https://api.sheety.co/9f51e04f70ac7da364035458aab4d70e/"
    "flightDeals/prices"
)


class DataManager:
    """Manage reading from and writing to the Google Sheets database."""

    def __init__(self) -> None:
        """Initialize the Sheety API client using environment variables."""
        self._user = os.environ["SHEETY_USERNAME"]
        self._password = os.environ["SHEETY_PASSWORD"]
        self._authorization = HTTPBasicAuth(
            self._user,
            self._password,
        )
        self.destination_data = []

    def get_destination_data(self) -> list:
        """
        Retrieve all destination records from Google Sheets.

        Returns:
            list: A list of destination dictionaries.
        """
        response = requests.get(
            SHEETY_ENDPOINT,
            auth=self._authorization,
        )

        self.destination_data = response.json()["prices"]
        return self.destination_data

    def update_lowest_price(
        self,
        row_id: int,
        new_price: float,
    ) -> None:
        """
        Update the lowest recorded flight price for a destination.

        Args:
            row_id: The row ID in the Google Sheet.
            new_price: The newly discovered lowest flight price.
        """
        payload = {
            "price": {
                "lowestPrice": new_price,
            }
        }

        response = requests.put(
            url=f"{SHEETY_ENDPOINT}/{row_id}",
            json=payload,
            auth=self._authorization,
        )

        if response.status_code == 200:
            print(
                f"Successfully updated destination {row_id} "
                f"with new price: GBP {new_price}"
            )
        else:
            print(f"Failed to update destination {row_id}.")
            print(f"Status Code: {response.status_code}")
            print(f"Response: {response.text}")
