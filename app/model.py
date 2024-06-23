from typing import Any, Optional, Union
from pydantic import BaseModel, Field
from datetime import date
from uuid import UUID, uuid4
import json


class Person(BaseModel):
    # Person.model_validate(<dict>) to create new instance from Dict
    # Person.model_validate_json(<json-str>) to create new instance from JSON
    # person.model_dump() to serialize to Dict
    # person.model_dump_json() to serialize to JSON
    person_id: UUID = Field(default_factory=uuid4, frozen=True)
    name: str = Field(min_length=1, frozen=True)
    dob: date = Field(frozen=True)
    occupation: Optional[str] = Field(default=None, frozen=True)
    height: Optional[Union[float, int]] = Field(default=None, gt=0, repr=True)


def create_flat_dct_from_person(person: Person) -> dict:
    """Creates a Serializable Python Dictionary from Person Object."""
    return json.loads(person.model_dump_json())


def create_person_from_dict(person_dict: dict) -> Person:
    return Person.model_validate(person_dict)
