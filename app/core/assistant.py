import json
import re
from app.core.llm_service import LLMService

class VoiceAssistant:

    def __init__(self):
        with open("orders.json") as f:
            self.orders = json.load(f)

        with open("policies.json") as f:
            self.policies = json.load(f)

        self.llm = LLMService()

    # ----------------------------
    # Intent Detection
    # ----------------------------
    def detect_intent(self, text):
        text = text.lower()

        if "order" in text:
            return "order_tracking"
        elif "return" in text:
            return "return_policy"
        elif "refund" in text:
            return "refund_policy"
        elif any(w in text for w in ["hour", "open", "support", "available", "timing"]):
            return "support_hours"
        else:
            return "unknown"

    # ----------------------------
    # Extract Order ID
    # ----------------------------
    def extract_order_id(self, text):
        # Match explicit ORD-prefixed IDs like "ORD124"
        match = re.search(r'ORD\d+', text, re.IGNORECASE)
        if match:
            return match.group(0).upper()

        # Extract any number sequence from the text
        # and check if it matches a real order ID in the data
        numbers = re.findall(r'\d+', text)
        all_order_ids = [o["order_id"] for o in self.orders]

        for num in numbers:
            # Try exact match (e.g. "887")
            if num in all_order_ids:
                return num
            # Try with ORD prefix (e.g. "ORD124")
            if f"ORD{num}" in all_order_ids:
                return f"ORD{num}"

        return None

    # ----------------------------
    # Handle Query
    # ----------------------------
    def handle_query(self, text, user_id="U1"):
        intent = self.detect_intent(text)
        context = {}

        if intent == "order_tracking":
            order_id = self.extract_order_id(text)

            if order_id:
                for order in self.orders:
                    if order["order_id"] == order_id and order["user_id"] == user_id:
                        context = order
                        break

            if not context:
                context = {"error": f"No order found with ID {order_id} for this account."}

        elif intent == "return_policy":
            context = self.policies["returns"]

        elif intent == "refund_policy":
            context = self.policies["refunds"]

        elif intent == "support_hours":
            context = {"support_hours": self.policies["support_hours"]}

        else:
            context = {"note": "No relevant data found. Tell the user you can help with orders, returns, refunds, and support hours."}

        return self.llm.generate_response(text, context)
