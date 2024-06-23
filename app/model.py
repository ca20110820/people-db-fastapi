from typing import Any, Optional, Union
from dataclasses import dataclass
from pydantic import BaseModel
import json
import hashlib
import base64


def _generate_short_uid(obj):
    obj_str = str(obj)
    hash_obj = hashlib.sha256(obj_str.encode()).digest()
    short_uid = base64.urlsafe_b64encode(hash_obj).decode('utf-8')[:6]
    return short_uid


@dataclass
class Person:
    person_id: str
    name: str
    dob: str
    occupation: Optional[str] = None
    height: Optional[Union[float, int]] = None

    def __init__(self,
                 id: str,
                 name: str,
                 dob: str,
                 occupation: Optional[str] = None,
                 height: Optional[Union[float, int]] = None
                 ):
        # TODO: Add Protection pattern
        self.person_id = id
        self.name = name
        self.dob = dob
        self.occupation = occupation
        self.height = height

    def __str__(self) -> str:
        return self.to_json_str(indent=4)

    @classmethod
    def create_with_uid(cls,
                        name: str,
                        dob: str,
                        occupation: Optional[str] = None,
                        height: Optional[Union[float, int]] = None
                        ) -> 'Person':
        obj = (
            name,
            dob,
            occupation,
            height
        )

        instance = cls(
            _generate_short_uid(obj),
            name,
            dob,
            occupation,
            height
        )

        return instance

    @classmethod
    def from_dict(cls, person_dict: dict) -> 'Person':
        instance = cls(
            person_dict['person_id'],
            person_dict['name'],
            person_dict['dob'],
            person_dict['occupation'],
            person_dict['height']
        )
        
        return instance

    def to_dict(self) -> dict:
        return {
            "person_id": self.person_id,
            "name": self.name,
            "dob": self.dob,
            "occupation": self.occupation,
            "height": self.height,
        }

    @classmethod
    def from_json_str(cls, json_str: str) -> 'Person':
        data_dict = json.loads(json_str)
        return cls.from_dict(data_dict)

    def to_json_str(self, *args, **kwargs) -> str:
        return json.dumps(self.to_dict(), *args, **kwargs)
