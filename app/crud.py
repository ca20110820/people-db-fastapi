from typing import List
from pathlib import Path
from tinydb import TinyDB, Query
import tinydb.operations as tdb_ops
import json

from model import Person


DB_PATH = Path(__file__).resolve().parent / 'data' / 'people.json'


class PeopleDB:
    def __init__(self):
        self.db_path = str(DB_PATH)

    def get_people(self) -> List[Person]:
        with TinyDB(self.db_path) as db:
            return [Person.from_json_str(json.dumps(doc)) for doc in db.all()]
    
    def get_person(self, person_id: str) -> Person:
        with TinyDB(self.db_path) as db:
            doc = db.get(Query().person_id == person_id)
            json_str = json.dumps(doc)
        return Person.from_json_str(json_str)
    
    def upsert_person(self, person: Person) -> None:
        dct = person.to_dict()
        with TinyDB(self.db_path) as db:
            db.upsert(dct, Query().person_id == str(dct["person_id"]))
    
    def delete_person(self, person: Person) -> None:
        with TinyDB(self.db_path) as db:
            db.remove(Query().person_id == person.person_id)


def get_people_json_str(people_db: PeopleDB) -> str:
    return json.dumps([person.to_dict() for person in people_db.get_people()])


p1 = Person.create_with_uid('Person1', '1999-06-25', 'Programmer', 182)
p2 = Person.create_with_uid('Person2', '2000-08-25', 'DevOps Engineer', 170)
p3 = Person.create_with_uid('Person3', '1995-03-2', 'Software Architect', 175)

people_db = PeopleDB()
people_db.upsert_person(p1)
people_db.upsert_person(p2)
people_db.upsert_person(p3)

people_db.delete_person(p2)

p1.occupation = "Senior DevOps Engineer"
people_db.upsert_person(p1)

p2 = Person.create_with_uid('Person2', '2000-08-25', 'DevOps Engineer', 170)
people_db.upsert_person(p2)

people = people_db.get_people()
for p in people:
    print(p)


print(get_people_json_str(people_db))
