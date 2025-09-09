# SHEETY API
import requests
import os
from dotenv import load_dotenv

load_dotenv("config.env.txt")

sheety_username = os.getenv("USERNAME_SHEETY")
sheety_password = os.getenv("PASSWORD_SHEETY")


class FlightData:
    # This class is responsible for structuring the flight data.
    def __init__(self):
        self.sheet_data = []
        self.customer_emails = []

    def load_sheet_data(self):
        response = requests.get(url="https://api.sheety.co/ceda0cce0844cfd4223effb29278e995/flightDealsFinder/prices",
                                auth=(sheety_username, sheety_password))

        data = response.json()
        print(data)
        self.sheet_data = data["prices"]  # converting this to a list, so we can later loop over to find the row which we have to put the iata code

    def load_iata_codes(self, city, cities_iata):
        for row in self.sheet_data:
            if row['city'] == city:  # if the city name from data is same as the city from cities_list
                row_id = row['id']  # we can fetch its id and put it in google sheet
                sheety_parameters = {'price': {'iataCode': cities_iata}}
                response = requests.put(url=f"https://api.sheety.co/ceda0cce0844cfd4223effb29278e995/flightDealsFinder/prices/{row_id}", json=sheety_parameters,
                                        auth=(sheety_username, sheety_password))
                break

    def get_customer_emails(self):
        response = requests.get(url="https://api.sheety.co/ceda0cce0844cfd4223effb29278e995/flightDealsFinder/users",
                                auth=(sheety_username, sheety_password))

        data = response.json()['users']
        for emails in data:
            self.customer_emails.append(emails['whatsYourEmail ?'])  # u could also use list comprehension to store the emails in the list instead of like this.
