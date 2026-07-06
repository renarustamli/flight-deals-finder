"""
Flight Search.

Handles communication with the SerpAPI Google Flights API to search
for available flights between two airports within a specified date range.
"""

import os

import requests
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

SERPAPI_ENDPOINT = "https://serpapi.com/search"


class FlightSearch:
    """Search for flights using the SerpAPI Google Flights API."""

    def __init__(self) -> None:
        """Initialize the flight search service with the SerpAPI key."""
        self._api_key = os.environ["SERPAPI_API_KEY"]

    def check_flights(
        self,
        origin_city_code: str,
        destination_city_code: str,
        from_time: datetime,
        to_time: datetime,
    ) -> dict | None:
        """
        Search for available round-trip flights.

        Args:
            origin_city_code: IATA code of the departure airport.
            destination_city_code: IATA code of the arrival airport.
            from_time: Departure date.
            to_time: Return date.

        Returns:
            The API response as a dictionary, or None if the request fails.
        """
        query = {
            "engine": "google_flights",
            "departure_id": origin_city_code,
            "arrival_id": destination_city_code,
            "outbound_date": from_time.strftime("%Y-%m-%d"),
            "return_date": to_time.strftime("%Y-%m-%d"),
            "type": "1",
            "adults": "1",
            "currency": "GBP",
            "api_key": self._api_key,
        }

        response = requests.get(
            url=SERPAPI_ENDPOINT,
            params=query,
        )

        if response.status_code != 200:
            print(f"API request failed ({response.status_code}).")
            return None

        data = response.json()

        # SerpAPI returns an "error" field when the request cannot be processed.
        if "error" in data:
            print(f"API error: {data['error']}")
            return None

        return data
