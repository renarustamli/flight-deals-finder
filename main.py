"""
Flight Deals Finder.

This application monitors flight prices for destinations stored in a
Google Sheet. It searches for available flights, compares the current
prices with the recorded lowest prices, updates the spreadsheet when
better deals are found, and sends notifications to the user.

Workflow:
1. Retrieve destination data from Google Sheets.
2. Search for flights within the next six months.
3. Identify the cheapest available flight.
4. Update the spreadsheet if a lower price is found.
5. Notify the user via WhatsApp (or SMS).
"""

from datetime import datetime, timedelta
from pprint import pprint

import requests_cache

from data_manager import DataManager
from flight_data import find_cheapest_flight
from flight_search import FlightSearch
from notification_manager import NotificationManager

ORIGIN_CITY_IATA = "LHR"


def main() -> None:
    """Run the Flight Deals Finder application."""

    # Cache flight search responses for one hour to reduce API requests.
    # Google Sheets data is intentionally excluded from caching so that
    # destination information is always up to date.
    requests_cache.install_cache(
        cache_name="flight_cache",
        expire_after=3600,
        backend="sqlite",
    )

    # Initialize application services.
    data_manager = DataManager()
    flight_search = FlightSearch()
    notification_manager = NotificationManager()

    # Retrieve the latest destination data.
    destinations = data_manager.get_destination_data()
    pprint(destinations)

    # Search for flights departing within the next six months.
    today = datetime.now()
    departure_date = today + timedelta(days=1)
    return_date = today + timedelta(days=180)

    for destination in destinations:
        pprint(f"Searching flights to {destination['city']}...")

        flights = flight_search.check_flights(
            origin_city_code=ORIGIN_CITY_IATA,
            destination_city_code=destination["iataCode"],
            from_time=departure_date,
            to_time=return_date,
        )

        cheapest_flight = find_cheapest_flight(
            flights,
            return_date=return_date.strftime("%Y-%m-%d"),
        )

        pprint(f"{destination['city']}: GBP {cheapest_flight.price}")

        # Update the stored price and notify the user only when a
        # better flight deal is found.
        if (
            cheapest_flight.price != "N/A"
            and cheapest_flight.price < destination["lowestPrice"]
        ):
            pprint(f"Lower price found for {destination['city']}!")

            data_manager.update_lowest_price(
                destination["id"],
                cheapest_flight.price,
            )

            message = (
                f"Low price alert! Only GBP {cheapest_flight.price} "
                f"to fly from {cheapest_flight.origin_airport} "
                f"to {cheapest_flight.destination_airport}, "
                f"on {cheapest_flight.out_date} "
                f"until {cheapest_flight.return_date}."
            )

            # WhatsApp is enabled by default. If you prefer SMS,
            # replace send_whatsapp() with send_sms().
            notification_manager.send_whatsapp(message)

            # notification_manager.send_sms(message)


if __name__ == "__main__":
    main()

