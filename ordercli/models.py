from typing import List
from marshmallow import Schema, fields, post_load


class Address:
    def __init__(self, city: str, postal_code: int, street: str) -> None:
        self.city = city
        self.postal_code = postal_code
        self.street = street


class AddressSchema(Schema):
    city = fields.Str()
    postal_code = fields.Int()
    street = fields.Str()

    @post_load
    def make_address(self, data, **kwargs):
        return Address(**data)


class Employee:
    def __init__(self, address: Address, name: str):
        self.address = address
        self.name = name


class EmployeeSchema(Schema):
    address = fields.Nested(AddressSchema)
    name = fields.Str()

    @post_load
    def make_employee(self, data, **kwargs):
        return Employee(**data)


class Order:
    def __init__(self, amount: int, id: int) -> None:
        self.id = id
        self.amount = amount


class OrderSchema(Schema):
    id = fields.Int()
    amount = fields.Int()

    @post_load
    def make_order(self, data, **kwargs):
        return Order(**data)


class EmployeeOrders:
    def __init__(self, employee: Employee, is_attending: bool, orders: List["Order"]):
        self.employee = employee
        self.is_attending = is_attending
        self.orders = orders


class EmployeeOrdersSchema(Schema):
    employee = fields.Nested(EmployeeSchema)
    is_attending = fields.Bool()
    orders = fields.List(fields.Nested(OrderSchema))

    @post_load
    def make_employee_orders(self, data, **kwargs):
        return EmployeeOrders(**data)
