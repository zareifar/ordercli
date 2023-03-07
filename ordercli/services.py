from typing import List, TextIO
import xml.etree.ElementTree as ET

from .models import (
    AddressSchema,
    EmployeeSchema,
    EmployeeOrders,
    EmployeeOrdersSchema,
    Order,
    OrderSchema,
)
from .typings import NourishMenu


def parse_orders(orders_str: str, menu: NourishMenu) -> List[Order]:
    """
    Parse orders within an item in the Employee orders XML file.
    Orders are comma separated in the provided string.

    Params:
        orders_str: A string of characters indicating the orders. The orders
                    can be separated by comma e.g. '1x Fried Chicken, 1x Caesar Salad'
        menu: Nourish menu

    Returns:
        A list of Order objects.
    """
    orders = []
    for order_str in orders_str.split(","):
        amount_str, dish_str = order_str.strip().split("x")
        orders.append(
            OrderSchema().load(
                {"amount": int(amount_str.strip()), "id": menu[dish_str.strip()]}
            )
        )

    return orders


def parse_xml_orders(file: TextIO, menu: NourishMenu) -> List[EmployeeOrders]:
    """
    Parse employee orders XML file and return a structured list of EmployeeOrders.

    Params:
        file: Employee orders XML file
        menu: Nourish menu

    Returns:
        A structured list of Employee orders
    """
    root = ET.parse(file).getroot()

    employee_orders = []
    dishes_ids = {dish["name"]: dish["id"] for dish in menu["dishes"]}

    for item in root.findall("Employee"):
        try:
            address = AddressSchema().load(
                {
                    "city": getattr(item.find("Address/City"), "text"),
                    "postal_code": int(
                        getattr(item.find("Address/PostalCode"), "text")
                    ),
                    "street": getattr(item.find("Address/Street"), "text"),
                }
            )
            orders = parse_orders(getattr(item.find("Order"), "text"), dishes_ids)
            employee = EmployeeSchema().load(
                {
                    "address": AddressSchema().dump(address),
                    "name": getattr(item.find("Name"), "text"),
                }
            )
            employee_order = EmployeeOrdersSchema().load(
                {
                    "employee": EmployeeSchema().dump(employee),
                    "is_attending": getattr(item.find("IsAttending"), "text"),
                    "orders": [OrderSchema().dump(order) for order in orders],
                }
            )

            employee_orders.append(employee_order)

        except AttributeError:
            continue

    return employee_orders
