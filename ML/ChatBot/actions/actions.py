import requests
import json
from io import BytesIO
from PIL import Image

from typing import Any, Text, Dict, List
import collections
import base64
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

import sqlite3
import random



class Queryticketprice(Action):

    def name(self) -> Text:
        return "query_landmark_ticketprice"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        conn = DbQueryingMethods.create_connection(db_file="landmarks.db")

        slot_value = tracker.get_slot("landmark")
        slot_name = "name"
        col = "ticket_price"

        get_query_results = DbQueryingMethods.select_by_slot(conn=conn,
            slot_name=slot_name,slot_value=slot_value,col = col)
        dispatcher.utter_message(text=str(get_query_results))

        return

class Querylocation(Action):

    def name(self) -> Text:
        return "query_landmark_location"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        conn = DbQueryingMethods.create_connection(db_file="landmarks.db")

        slot_value = tracker.get_slot("landmark")
        slot_name = "name"
        col = "location_link"

        get_query_results = DbQueryingMethods.select_by_slot(conn=conn,
            slot_name=slot_name,slot_value=slot_value,col = col)
        dispatcher.utter_message(text=str(get_query_results))

        return

class Querydescription(Action):

    def name(self) -> Text:
        return "query_landmark_description"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        conn = DbQueryingMethods.create_connection(db_file="landmarks.db")

        slot_value = tracker.get_slot("landmark")
        slot_name = "name"
        col = "description2"

        get_query_results = DbQueryingMethods.select_by_slot(conn=conn,
            slot_name=slot_name,slot_value=slot_value,col = col)
        dispatcher.utter_message(text=str(get_query_results))

        return

class Queryopeninghours(Action):

    def name(self) -> Text:
        return "query_landmark_openinghours"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        conn = DbQueryingMethods.create_connection(db_file="landmarks.db")

        slot_value = tracker.get_slot("landmark")
        slot_name = "name"
        col = "opening_hours"

        get_query_results = DbQueryingMethods.select_by_slot(conn=conn,
            slot_name=slot_name,slot_value=slot_value,col = col)
        dispatcher.utter_message(text=str(get_query_results))

        return

class Queryactivity(Action):

    def name(self) -> Text:
        return "query_landmark_activity"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        conn = DbQueryingMethods.create_connection(db_file="landmarks.db")

        slot_value = tracker.get_slot("landmark")
        slot_name = "name"
        col = "activity"

        get_query_results = DbQueryingMethods.select_by_slot(conn=conn,
            slot_name=slot_name,slot_value=slot_value,col = col)
        dispatcher.utter_message(text=str(get_query_results))

        return

class DbQueryingMethods:
    def create_connection(db_file):
        """
        create a database connection to the SQLite database
        specified by the db_file
        :param db_file: database file
        :return: Connection object or None
        """
        conn = None
        try:
            conn = sqlite3.connect(db_file)
        except Error as e:
            print(e)

        return conn

    def select_by_slot(conn, slot_name, slot_value,col):
        """
        Query all rows in the tasks table
        :param conn: the Connection object
        :return:
        """
        cur = conn.cursor()
        cur.execute(f'''SELECT {col} FROM landmarks
                    WHERE {slot_name}="{slot_value}"''')

        # return an array
        rows = cur.fetchall()
        if len(list(rows)) < 1:
            return "There are no resources matching your query."
        else:
            return(rows[0][0])







class ActionClassifyPlace(Action):
    def name(self):
        return "action_classify_place"

    def run(self, dispatcher, tracker, domain):
        # Get the URL of the image from the user input
        place_url = tracker.get_slot("place_url")

        # Send a GET request to the API to retrieve the image
        image_response = requests.get(place_url)

        files = {'image': image_response.content}
        # Send a POST request to the API to classify the image
        api_url = "https://942b-156-199-176-242.ngrok-free.app/places_api/ocr-translate/"
        response = requests.post(api_url, files=files)

        if response.status_code == 200:
            result = response.json()

            dispatcher.utter_message(f"This place is {result}.")
        else:
            dispatcher.utter_message("Sorry, I could not read the image at this time.")

        return []

class ActionStorePlaceURL(Action):
    def name(self) -> Text:
        return "action_store_place_url"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Extract the place URL entity from the user's input
        place_url = tracker.latest_message['text']

        # Store the place URL in the "image_url" slot
        if place_url:
            SlotSet('place_url', place_url)
            dispatcher.utter_message(text=f"Got it, I'll use this image: {place_url}")
        else:
            dispatcher.utter_message(text="Sorry, I didn't catch the image URL. Can you please try again?")

        return []

class ActionResetPlace(Action):

    def name(self) -> Text:
        return "action_reset_place"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        return [SlotSet("place_url", None)]

class ActionExtractText(Action):
    def name(self):
        return "action_extract_text"

    def run(self, dispatcher, tracker, domain):
        # Get the URL of the image from the user input
        image_url = tracker.get_slot("image_url")

        # Send a GET request to the API to retrieve the image
        image_response = requests.get(image_url)

        files = {'image': image_response.content}
        # Send a POST request to the API to classify the image
        api_url = "https://942b-156-199-176-242.ngrok-free.app/places_api/ocr-translate/"
        response = requests.post(api_url, files=files)

        if response.status_code == 200:
            result = response.json()

            dispatcher.utter_message(f"The text is {result}.")
        else:
            dispatcher.utter_message("Sorry, I could not read the text at this time.")

        return []

class ActionStoreImageURL(Action):
    def name(self) -> Text:
        return "action_store_image_url"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Extract the image URL entity from the user's input
        image_url = tracker.latest_message['text']

        # Store the image URL in the "image_url" slot
        if image_url:
            SlotSet('image_url', image_url)
            dispatcher.utter_message(text=f"Got it, I'll use this image: {image_url}")
        else:
            dispatcher.utter_message(text="Sorry, I didn't catch the image URL. Can you please try again?")

        return []

class ActionResetImage(Action):

    def name(self) -> Text:
        return "action_reset_image"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        return [SlotSet("image_url", None)]
