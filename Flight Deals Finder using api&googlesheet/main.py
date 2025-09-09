import flight_search
import flight_data
import notification_manager

flight_search = flight_search.FlightSearch()
sheet_data = flight_data.FlightData()

sheet_data.load_sheet_data()
print(sheet_data.sheet_data)
sheet_data.get_customer_emails()
print(sheet_data.customer_emails)

for city in sheet_data.sheet_data:
    city_name = city['city']
    lowest_price = city['lowestPrice']
    sheet_cities_iata = flight_search.get_iata_location(city_name)
    sheet_data.load_iata_codes(city_name, sheet_cities_iata)
    flights = flight_search.check_flight(sheet_cities_iata, "true")
    cheapest_flight = flight_search.find_cheapest_flight(flights)

    if not cheapest_flight:
        flights = flight_search.check_flight(sheet_cities_iata, "false")
        cheapest_flight = flight_search.find_cheapest_flight(flights)

    if cheapest_flight and cheapest_flight['price'] < lowest_price:   # if not none and using cheapest_flight dictionary of the updated price < sheet price.
        print(f"Cheapest flight found for {city_name}:")
        print(f"Price: {cheapest_flight['price']}")
        print(f"Departure IATA: {cheapest_flight['departure_iata']}")
        print(f"Arrival IATA: {cheapest_flight['arrival_iata']}")
        print(f"Out Date: {cheapest_flight['out_date']}")
        print(f"Return Date: {cheapest_flight['return_date']}")
        print(f"Number of Stops: {cheapest_flight['num_stops']}")

        send_sms = notification_manager.NotificationManager()
        message = (f"Low price alert! Only £{cheapest_flight['price']} to "
                   f"fly from {cheapest_flight['departure_iata']} to {cheapest_flight['arrival_iata']}, "
                   f"on {cheapest_flight['out_date']} until {cheapest_flight['return_date']}. "
                   f"Number of Stops : {cheapest_flight['num_stops']}")
        send_sms.send_sms(message)

        email_message = (f"Low price alert!\nOnly £{cheapest_flight['price']} to fly from {cheapest_flight['departure_iata']} to {cheapest_flight['arrival_iata']}, "
                         f"\non {cheapest_flight['out_date']} until {cheapest_flight['return_date']}. "
                         f"\nNumber of Stops : {cheapest_flight['num_stops']}")

        send_sms.send_emails(email_message, sheet_data.customer_emails)

    else:
        print(f"No Flights available at your lowest price for {city_name}")
