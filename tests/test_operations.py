import csv
import json
import os
from datetime import datetime

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from random_users.db_classes import Base, Location, Picture, User
from random_users.operations import dump_to_csv, insert_user_data, query_users


@pytest.fixture(autouse=True)
def test_db():
    engine = create_engine("sqlite:///:memory:")
    Session = sessionmaker(bind=engine)
    session = Session()
    Base.metadata.create_all(engine)
    yield session


@pytest.fixture(scope="module")
def test_data():
    return {
        "results": [
            {
                "gender": "female",
                "name": {"title": "Miss", "first": "Jennie", "last": "Nichols"},
                "location": {
                    "street": {
                        "number": 8929,
                        "name": "Valwood Pkwy",
                    },
                    "city": "Billings",
                    "state": "Michigan",
                    "country": "United States",
                    "postcode": "63104",
                    "coordinates": {"latitude": "-69.8246", "longitude": "134.8719"},
                    "timezone": {"offset": "+9:30", "description": "Adelaide, Darwin"},
                },
                "email": "jennie.nichols@example.com",
                "login": {
                    "uuid": "7a0eed16-9430-4d68-901f-c0d4c1c3bf00",
                    "username": "yellowpeacock117",
                    "password": "addison",
                    "salt": "sld1yGtd",
                    "md5": "ab54ac4c0be9480ae8fa5e9e2a5196a3",
                    "sha1": "edcf2ce613cbdea349133c52dc2f3b83168dc51b",
                    "sha256": "48df5229235ada28389b91e60a935e4f9b73eb4bdb855ef9258a1751f10bdc5d",
                },
                "dob": {"date": "1992-03-08T15:13:16.688Z", "age": 30},
                "registered": {"date": "2007-07-09T05:51:59.390Z", "age": 14},
                "phone": "(272) 790-0888",
                "cell": "(489) 330-2385",
                "id": {"name": "SSN", "value": "405-88-3636"},
                "picture": {
                    "large": "https://randomuser.me/api/portraits/men/75.jpg",
                    "medium": "https://randomuser.me/api/portraits/med/men/75.jpg",
                    "thumbnail": "https://randomuser.me/api/portraits/thumb/men/75.jpg",
                },
                "nat": "US",
            }
        ],
        "info": {"seed": "56d27f4a53bd5441", "results": 1, "page": 1, "version": "1.4"},
    }


def test_insert_user_data(test_db, test_data):
    insert_user_data(test_db, test_data)
    user = test_db.query(User).first()
    location = test_db.query(Location).first()
    picture = test_db.query(Picture).first()
    assert user.last_name == "Nichols"
    assert user.date_of_birth == datetime(1992, 3, 8, 15, 13, 16, 688000)
    assert location.city == "Billings"
    assert location.postcode == "63104"
    assert picture.large == "https://randomuser.me/api/portraits/men/75.jpg"


def test_query_users_no_filter(test_db, test_data):
    insert_user_data(test_db, test_data)
    users = json.loads(query_users(test_db))
    assert len(users) == 1


def test_query_users_filter_last_name(test_db, test_data):
    insert_user_data(test_db, test_data)
    users = json.loads(query_users(test_db, [("last_name", "Nichols")]))
    assert len(users) == 1


def test_query_users_filter_no_match(test_db, test_data):
    insert_user_data(test_db, test_data)
    users = json.loads(query_users(test_db, [("last_name", "Smith")]))
    assert len(users) == 0


def test_query_user_filter_location(test_db, test_data):
    insert_user_data(test_db, test_data)
    users = json.loads(query_users(test_db, [("city", "Billings")]))
    assert len(users) == 1


def test_export_to_csv(test_db, test_data):
    insert_user_data(test_db, test_data)
    dump_to_csv(test_db, "test.csv")
    with open("test.csv") as f:
        reader = csv.reader(f)
        rows = list(reader)
    assert len(rows) == 1
    assert rows[0][4] == "Nichols"
    assert rows[0][3] == "Jennie"
    os.remove("test.csv")
