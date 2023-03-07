import pytest
import xml.etree.ElementTree as ET
from io import StringIO


from ordercli.models import (
    Address,
    Employee,
    EmployeeOrders,
    EmployeeOrdersSchema,
    Order,
)
from ordercli.services import parse_xml_orders


@pytest.fixture
def menu():
    return {
        "dishes": [
            {"id": 1, "name": "Hamburger"},
            {"id": 2, "name": "Fries"},
            {"id": 3, "name": "Salad"},
            {"id": 4, "name": "Water"},
            {"id": 5, "name": "Soda"},
        ]
    }


@pytest.fixture
def xml_file():
    xml_string = """
    <Employees>
        <Employee>
            <Name>John Doe</Name>
            <Address>
                <Street>123 Main St</Street>
                <City>Anytown</City>
                <PostalCode>12345</PostalCode>
            </Address>
            <IsAttending>true</IsAttending>
            <Order>1x Hamburger,2x Fries,2x Soda</Order>
        </Employee>
        <Employee>
            <Name>Jane Smith</Name>
            <Address>
                <Street>456 Elm St</Street>
                <City>Anytown</City>
                <PostalCode>54321</PostalCode>
            </Address>
            <IsAttending>false</IsAttending>
            <Order>2x Salad,1x Water</Order>
        </Employee>
    </Employees>
    """
    return StringIO(xml_string)


def test_parse_xml_orders(xml_file, menu):
    expected_employee_orders = [
        EmployeeOrders(
            employee=Employee(
                name="John Doe",
                address=Address(
                    street="123 Main St",
                    city="Anytown",
                    postal_code=12345,
                ),
            ),
            is_attending=True,
            orders=[
                Order(id=1, amount=1),
                Order(id=2, amount=2),
                Order(id=5, amount=2),
            ],
        ),
        EmployeeOrders(
            employee=Employee(
                name="Jane Smith",
                address=Address(
                    street="456 Elm St",
                    city="Anytown",
                    postal_code=54321,
                ),
            ),
            is_attending=False,
            orders=[
                Order(id=3, amount=2),
                Order(id=4, amount=1),
            ],
        ),
    ]

    parsed_orders = parse_xml_orders(xml_file, menu)

    assert len(parsed_orders) == len(expected_employee_orders)
    for i, item in enumerate(parsed_orders):
        assert EmployeeOrdersSchema().dumps(item) == EmployeeOrdersSchema().dumps(
            expected_employee_orders[i]
        )


def test_parse_xml_orders_empty_file(tmp_path, menu):
    with pytest.raises(ET.ParseError):
        empty_file = tmp_path / "empty.xml"
        empty_file.write_text("")
        parse_xml_orders(empty_file, menu)


def test_parse_xml_orders_invalid_file(menu):
    invalid_file = StringIO(
        "<InvalidXml><Employee><Name>John Doe</Name></Employee></InvalidXml>"
    )
    assert parse_xml_orders(invalid_file, menu) == []


def test_parse_xml_orders_missing_elements(xml_file, menu):
    xml_string = """
    <Employees>
        <Employee>
            <Name>John Doe</Name>
            <Address>
                <Street>123 Main St</Street>
            </Address>
            <Order>Hamburger, Fries</Order>
        </Employee>
    </Employees>
    """
    file = StringIO(xml_string)

    assert parse_xml_orders(file, menu) == []
