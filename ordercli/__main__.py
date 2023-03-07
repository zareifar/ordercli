import sys
import json

from .api import NourishClient
from .services import parse_xml_orders


def main():
    (file_path,) = sys.argv[1:]

    with open("config.json", "r") as f:
        config = json.load(f)

    nourish_client = NourishClient(config)
    menu = nourish_client.get_menu()

    with open(file_path, "r") as f:
        employee_orders = parse_xml_orders(f, menu)

    response = nourish_client.place_order(employee_orders)

    if response.status_code == 202:
        print("Orders were placed!")


if __name__ == "__main__":
    main()
