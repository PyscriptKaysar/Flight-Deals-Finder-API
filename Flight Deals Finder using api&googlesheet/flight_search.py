import requests
import os
from dotenv import load_dotenv
import datetime
from dateutil.relativedelta import relativedelta


load_dotenv("config.env.txt")

API_KEY = os.getenv("AMADEUS_API_KEY")
API_SECRET = os.getenv("AMADEUS_API_SECRET")


class FlightSearch:
    # This class is responsible for talking to the Flight Search API.

    def __init__(self):
        self.amadeus_token = self.get_new_token()
        self.auth_header = {"authorization": f"Bearer {self.amadeus_token}"}

    def get_new_token(self):
        flight_search_headers = {"Content-type": "application/x-www-form-urlencoded"}
        flight_search_body = {"grant_type": "client_credentials", "client_id": API_KEY, "client_secret": API_SECRET}
        response = requests.post(url="https://test.api.amadeus.com/v1/security/oauth2/token",
                                 headers=flight_search_headers, data=flight_search_body)
        data = response.json()
        amadeus_token = data['access_token']
        print(data)
        return amadeus_token

    def get_iata_location(self, city_name):
        iata_parameters = {"keyword": city_name, "max": 2, "include": "AIRPORTS"}
        iata_headers = self.auth_header
        response = requests.get(url="https://test.api.amadeus.com/v1/reference-data/locations/cities", params=iata_parameters, headers=iata_headers)
        data = response.json()
        return data['data'][0]['iataCode']

    def check_flight(self, city_iata, is_direct):
        today = datetime.datetime.now()
        tomorrow = today + datetime.timedelta(1)
        six_months = today + relativedelta(months=+6)
        origin_location_iata = "LON"
        flight_search_parameters = {"originLocationCode": origin_location_iata, "destinationLocationCode": city_iata,
                                    "departureDate": tomorrow.strftime('%Y-%m-%d'), "returnDate": six_months.strftime('%Y-%m-%d'), "adults": 1,
                                    "currencyCode": "GBP", "max": 10, "nonStop": is_direct}

        flight_search_headers = self.auth_header
        response = requests.get(url="https://test.api.amadeus.com/v2/shopping/flight-offers",
                                params=flight_search_parameters, headers=flight_search_headers)
        data = response.json()
        print(data)
        return data

    def find_cheapest_flight(self, flight_data):
        cheapest_flight = None  # storing this variable to check later in main.py
        for flights in flight_data["data"]:  # flight_data is the check_flight data
            price = float(flights["price"]["grandTotal"])
            departure_iata = flights["itineraries"][0]["segments"][0]["departure"]["iataCode"]
            arrival_iata = flights["itineraries"][0]["segments"][0]["arrival"]["iataCode"]
            if len(flights['itineraries'][0]['segments']) - 1 == 1:          # arrival iata of the final destination for 1 stop
                arrival_iata = flights["itineraries"][0]["segments"][1]["arrival"]["iataCode"]
            elif len(flights['itineraries'][0]['segments']) - 1 == 2:       # arrival iata if the final destination for 2 stops
                arrival_iata = flights["itineraries"][0]["segments"][2]["arrival"]["iataCode"]
            out_date = flights["itineraries"][0]["segments"][0]["departure"]["at"].split('T')[0]
            return_date = flights["itineraries"][1]["segments"][0]["departure"]["at"].split('T')[0]
            num_stops = len(flights["itineraries"][0]["segments"]) - 1
            print(price)
            print(departure_iata)
            print(arrival_iata)
            print(out_date)
            print(return_date)
            print(num_stops)
            if cheapest_flight is None or price < cheapest_flight['price']:  # if no flights have been checked or
                cheapest_flight = {                                          # if the current flight price is lower than the previous flights
                    "price": price,
                    "departure_iata": departure_iata,           # a dictionary to update the current flight details if it's lower than previous
                    "arrival_iata": arrival_iata,
                    "out_date": out_date,
                    "return_date": return_date,
                    "num_stops": num_stops
                }
        return cheapest_flight
