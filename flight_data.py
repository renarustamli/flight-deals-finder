"""
Flight Data.

Represents flight information and provides a helper function to
identify the cheapest flight returned by the SerpAPI response.
"""


class FlightData:
    """Store information about a flight offer."""

    def __init__(
        self,
        price,
        origin_airport,
        destination_airport,
        out_date,
        return_date,
    ) -> None:
        """
        Initialize a flight offer.

        Args:
            price: Flight price in GBP.
            origin_airport: Departure airport IATA code.
            destination_airport: Arrival airport IATA code.
            out_date: Outbound flight date.
            return_date: Return flight date.
        """
        self.price = price
        self.origin_airport = origin_airport
        self.destination_airport = destination_airport
        self.out_date = out_date
        self.return_date = return_date


def find_cheapest_flight(data, return_date) -> FlightData:
    """
    Find the cheapest available flight from the API response.

    Args:
        data: JSON response returned by SerpAPI.
        return_date: Return flight date.

    Returns:
        A FlightData object containing the cheapest flight found.
        If no flights are available, returns a FlightData object
        with "N/A" values.
    """
    if data is None:
        print("No flight data available.")
        return FlightData("N/A", "N/A", "N/A", "N/A", "N/A")

    all_flights = (
        data.get("best_flights", [])
        + data.get("other_flights", [])
    )

    if not all_flights:
        print("No flights found.")
        return FlightData("N/A", "N/A", "N/A", "N/A", "N/A")

    first_flight = all_flights[0]

    lowest_price = first_flight["price"]
    origin = first_flight["flights"][0]["departure_airport"]["id"]
    destination = first_flight["flights"][-1]["arrival_airport"]["id"]
    out_date = (
        first_flight["flights"][0]["departure_airport"]["time"]
        .split(" ")[0]
    )

    cheapest_flight = FlightData(
        lowest_price,
        origin,
        destination,
        out_date,
        return_date,
    )

    for flight in all_flights:
        try:
            price = flight["price"]
        except KeyError:
            # Some API responses may omit price information.
            continue

        if price < lowest_price:
            lowest_price = price
            origin = flight["flights"][0]["departure_airport"]["id"]
            destination = flight["flights"][-1]["arrival_airport"]["id"]
            out_date = (
                flight["flights"][0]["departure_airport"]["time"]
                .split(" ")[0]
            )

            cheapest_flight = FlightData(
                lowest_price,
                origin,
                destination,
                out_date,
                return_date,
            )

            print(
                f"Lowest price to {destination} "
                f"is GBP {lowest_price}"
            )

    return cheapest_flight