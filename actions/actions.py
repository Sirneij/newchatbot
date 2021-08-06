from typing import Any, Dict, List, Text

import requests
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher


class ActionProductSearch(Action):
    def name(self) -> Text:
        return "action_product_search"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        # get slots and save as tuple
        device = [(tracker.get_slot("brand")), (tracker.get_slot("name"))]

        if device[0] and device[1]:
            # both name and brand
            response = requests.get(
                "https://futahub.herokuapp.com/api/products/{}/{}/".format(device[1], device[0])
            )
        if device[0]:
            # only brand
            response = requests.get(
                "https://futahub.herokuapp.com/api/products/brands/{}".format(device[0])
            )

        if device[1]:
            # only name
            response = requests.get("https://futahub.herokuapp.com/api/products/{}".format(device[1]))

        else:
            response = {}

        if response:
            # provide in stock message
            dispatcher.utter_message(response="utter_in_stock")
            slots_to_reset = ["name", "brand"]
            return [SlotSet(slot, None) for slot in slots_to_reset]
        else:
            # provide out of stock
            dispatcher.utter_message(response="utter_no_stock")
            slots_to_reset = ["name", "brand"]
            return [SlotSet(slot, None) for slot in slots_to_reset]


class SurveySubmit(Action):
    def name(self) -> Text:
        return "action_survey_submit"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(response="utter_open_feedback")
        dispatcher.utter_message(response="utter_survey_end")
        return [SlotSet("survey_complete", True)]


class OrderStatus(Action):
    def name(self) -> Text:
        return "action_order_status"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        # get email and order_id slot
        order_email_id = (
            tracker.get_slot("email"),
            tracker.get_slot("order_id"),
        )
        if order_email_id[0] and order_email_id[1]:
            respons_order = requests.get(
                "https://futahub.herokuapp.com/api/order-single/{}/{}/".format(
                    order_email_id[1], order_email_id[0]
                )
            )
        if order_email_id[1]:
            respons_order = requests.get(
                "https://futahub.herokuapp.com/api/order/{}/".format(order_email_id[1])
            )
        if order_email_id[0]:
            respons_order = requests.get(
                "https://futahub.herokuapp.com/api/orders/emails/{}/".format(order_email_id[0])
            )
        else:
            respons_order = {}
        if respons_order:
            resj = respons_order.json()
            if resj["order_is_received"]:
                status = "your order has been received and being processed."

            if resj["being_delivered"]:
                status = "your order has been processed and is being delivered."
            if resj["refund_requested"]:
                status = "you have requested a refund for this order."
            if resj["refund_granted"]:
                status = "your refund request for this order has been granted. Be on a lookout for disbursement."
            if not resj["paid"]:
                status = "you have not paid for this order. Until payment is made, this order will not be processed!"

            if resj["ordered"]:
                status = "your order is undergoing pre-processing."

        if respons_order:
            # respond with order status
            dispatcher.utter_message(response="utter_order_status", status=status)
            return []
        else:
            dispatcher.utter_message(response="utter_no_order")
            return []


class CancelOrder(Action):
    def name(self) -> Text:
        return "action_cancel_order"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        # get email and order_id slot
        order_email_id = (
            tracker.get_slot("email"),
            tracker.get_slot("order_id"),
        )
        if order_email_id[0] and order_email_id[1]:
            respons_order = requests.get(
                "https://futahub.herokuapp.com/api/order-single/{}/{}/".format(
                    order_email_id[1], order_email_id[0]
                )
            )
        elif order_email_id[1]:
            respons_order = requests.get(
                "https://futahub.herokuapp.com/api/order/{}/".format(order_email_id[1])
            )
        elif order_email_id[0]:
            respons_order = requests.get(
                "https://futahub.herokuapp.com/api/orders/emails/{}/".format(order_email_id[0])
            )
        else:
            respons_order = {}

        if respons_order:
            # # change status of entry
            # status = [("cancelled"), (tracker.get_slot("email"))]
            # cursor.execute("UPDATE orders SET status=? WHERE order_email=?", status)
            # connection.commit()
            # connection.close()

            # confirm cancellation
            dispatcher.utter_message(response="utter_order_cancel_finish")
            return []
        else:
            # db didn't have an entry with this email
            dispatcher.utter_message(response="utter_no_order")
            return []


class ReturnOrder(Action):
    def name(self) -> Text:
        return "action_return"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        # get email and order_id slot
        order_email_id = (
            tracker.get_slot("email"),
            tracker.get_slot("order_id"),
        )
        if order_email_id[0] and order_email_id[1]:
            respons_order = requests.get(
                "https://futahub.herokuapp.com/api/order-single/{}/{}/".format(
                    order_email_id[1], order_email_id[0]
                )
            )
        if order_email_id[1]:
            respons_order = requests.get(
                "https://futahub.herokuapp.com/api/order/{}/".format(order_email_id[1])
            )
        if order_email_id[0]:
            respons_order = requests.get(
                "https://futahub.herokuapp.com/api/orders/emails/{}/".format(order_email_id[0])
            )
        else:
            respons_order = {}

        if respons_order:
            # change status of entry
            # status = [("returning"), (tracker.get_slot("email"))]
            # cursor.execute("UPDATE orders SET status=? WHERE order_email=?", status)
            # connection.commit()
            # connection.close()

            # confirm return
            dispatcher.utter_message(response="utter_return_finish")
            return []
        else:
            # db didn't have an entry with this email
            dispatcher.utter_message(response="utter_no_order")
            return []
