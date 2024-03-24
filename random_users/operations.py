from __future__ import annotations

import csv
import json
from datetime import datetime
from typing import Any, Dict, List, Tuple

import requests
from sqlalchemy.orm import Session

from random_users.db_classes import Location, Picture, User


def get_user_data_api(results: int = 5000) -> Dict[str, Any]:
    response = requests.get(f"https://randomuser.me/api/?results={results}")
    if response.status_code != 200:
        raise SystemExit("Error retrieving the user data")

    return response.json()


def insert_user_data(session: Session, data: Dict[str, Any]) -> None:
    users = []
    for item in data["results"]:
        user = User(
            gender=item["gender"],
            title=item["name"]["title"],
            first_name=item["name"]["first"],
            last_name=item["name"]["last"],
            email=item["email"],
            uuid=item["login"]["uuid"],
            username=item["login"]["username"],
            password=item["login"]["password"],
            salt=item["login"]["salt"],
            md5=item["login"]["md5"],
            sha1=item["login"]["sha1"],
            sha256=item["login"]["sha256"],
            date_of_birth=datetime.fromisoformat(item["dob"]["date"]),
            registered=datetime.fromisoformat(item["registered"]["date"]),
            phone=item["phone"],
            cell=item["cell"],
            id_type=item["id"]["name"],
            id_value=item["id"]["value"],
            nationality=item["nat"],
        )
        users.append(user)

        location = Location(
            user=user,
            number=item["location"]["street"]["number"],
            street=item["location"]["street"]["name"],
            city=item["location"]["city"],
            state=item["location"]["state"],
            country=item["location"]["country"],
            postcode=item["location"]["postcode"],
            latitude=float(item["location"]["coordinates"]["latitude"]),
            longitude=float(item["location"]["coordinates"]["longitude"]),
            tz_offset=item["location"]["timezone"]["offset"],
            tz_desc=item["location"]["timezone"]["description"],
        )
        user.locations.append(location)

        picture = Picture(
            user=user,
            large=item["picture"]["large"],
            medium=item["picture"]["medium"],
            thumbnail=item["picture"]["thumbnail"],
        )
        user.pictures.append(picture)

    session.add_all(users)
    session.commit()
    session.close()


def query_users(session: Session, filters: List[Tuple[str, str]] | None = None):
    """Query the database and apply any filters provided by the `filters`
    parameter. Returns the results as a JSON list of objects."""
    result = session.query(User, Location, Picture).join(Location).join(Picture)
    if filters:
        for filt in filters:
            conditions = []
            key, value = filt
            for table in [User, Location, Picture]:
                try:
                    condition = getattr(table, key) == value
                    conditions.append(condition)
                    break
                except AttributeError:
                    pass
            result = result.filter(*conditions)
    result = result.all()
    session.close()
    # convert query result to list of dicts and convert to json
    return json.dumps(
        [
            {
                **{
                    col.name: getattr(row.User, col.name)
                    for col in row.User.__table__.columns
                },
                **{
                    col.name: getattr(row.Location, col.name)
                    for col in row.Location.__table__.columns
                },
                **{
                    col.name: getattr(row.Picture, col.name)
                    for col in row.Picture.__table__.columns
                },
            }
            for row in result
        ],
        default=str,
    )


def dump_to_csv(session: Session, path: str) -> None:
    """Exports all users to a csv file in `path`."""
    with open(path, "w") as out_file:
        out_csv = csv.writer(out_file)
        for user, location, picture in (
            session.query(User, Location, Picture).join(Location).join(Picture).all()
        ):
            row = (
                [getattr(user, col.name) for col in user.__table__.columns]
                + [getattr(location, col.name) for col in location.__table__.columns]
                + [getattr(picture, col.name) for col in picture.__table__.columns]
            )
            out_csv.writerow(row)
