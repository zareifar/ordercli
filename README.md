# OrderCli

This CLI tool parses the employee orders provided by an XML file and sends the orders to partners API. Since Nourish.me API is not a functioning API, this behavior was simulated by a mock API.

Project dependecies:

In this project [Marshmallow](https://marshmallow.readthedocs.io/en/stable/index.html) was used for serializing/deserialing data and data validation, and [Requests](https://requests.readthedocs.io/en/latest/) was used to handle requests.

## usage

To use the app, create a virtual environment and install the dependencies using the command below:

`pip install -r requirements.txt`

Run the tool using this command:

`python ordercli </path/to/employee_orders.xml>`

Run the tests using this command:

`pytest tests`
