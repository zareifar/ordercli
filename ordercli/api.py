import json
import requests
from typing import List

from .models import EmployeeSchema, EmployeeOrders, OrderSchema
from .typings import NourishMenu


class NourishClient:
    def __init__(self, config) -> None:
        self.config = config

    def get_menu(self) -> NourishMenu:
        response = requests.get(self.config["nourish.me"]["menu_url"])
        return response.json()

    def _generate_json_payload(self, employee_orders: List[EmployeeOrders]):
        return json.dumps(
            {
                "orders": [
                    {
                        "customer": EmployeeSchema().dump(order.employee),
                        "items": [OrderSchema().dump(order) for order in order.orders],
                    }
                    for order in employee_orders
                    if order.is_attending
                ]
            }
        )

    def place_order(self, employee_orders):
        response = requests.post(
            self.config["nourish.me"]["bulk_order_url"],
            data=self._generate_json_payload(employee_orders),
        )

        return response
