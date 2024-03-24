# random_users

This is a simple project that uses the [Random User Generator API](https://randomuser.me/) to generate random users, store them in a database and query them.

## Installation

1. Clone the repository
2. Create a Python virtual environment and activate it
3. Install the project with `pip install .`

## Usage
Inside the virtual environment, you can run the following commands:
* `random-users import-users` to import random users from the API
* `random-users export-users` to export the users to a CSV file
* `random-users show-users` to query the users in the database in JSON format

The `show-users` command accepts an arbitrary number of arguments that are used to filter the users. For example, `random-users show-users last_name=Smith` will show only the users with the last name "Smith".

## Contributing
Install the project in development mode with `pip install -e .[devel]`. This will install the necessary dependencies for testing and linting.

To run unit tests: `python -m pytest tests/`

Install `pre-commit` hooks with `pre-commit install` to run the linters before each commit.

