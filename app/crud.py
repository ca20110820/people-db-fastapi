from typing import List
from pathlib import Path
from tinydb import TinyDB, Query
import tinydb.operations as tdb_ops
import json


try:
    from app.model import Person
except ModuleNotFoundError:
    from model import Person


DB_PATH = Path(__file__).resolve().parent / 'data' / 'people.json'


class PeopleDB:
    def __init__(self):
        self.db_path = str(DB_PATH)

    def get_people(self) -> List[Person]:
        with TinyDB(self.db_path) as db:
            # return [Person.from_json_str(json.dumps(doc)) for doc in db.all()]
            return [Person.from_dict(doc) for doc in db.all()]

    def get_person(self, person_id: str) -> Person:
        with TinyDB(self.db_path) as db:
            doc = db.get(Query().person_id == person_id)
            json_str = json.dumps(doc)
        return Person.from_json_str(json_str)

    def insert_person(self, new_person_dict: dict) -> None:
        # Note: We assume that new_person_dict does not have 'person_id'
        with TinyDB(self.db_path) as db:
            db.insert(new_person_dict)

    def upsert_person(self, person: Person) -> None:
        dct = person.to_dict()
        with TinyDB(self.db_path) as db:
            db.upsert(dct, Query().person_id == str(dct["person_id"]))

    def delete_person(self, person: Person) -> None:
        with TinyDB(self.db_path) as db:
            db.remove(Query().person_id == person.person_id)

    def delete_person_by_id(self, person_id: str) -> None:
        with TinyDB(self.db_path) as db:
            db.remove(Query().person_id == person_id)


def get_people_json_str(people_db: PeopleDB) -> str:
    return json.dumps([person.to_dict() for person in people_db.get_people()])
