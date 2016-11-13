import uuid
import datetime

from src.common.database import Database
from src.models.goed import Goed


class Zaak(object):
    def __init__(self, zaaknaam, omschrijving):
        self.zaaknaam = zaaknaam
        self.omschrijving = omschrijving

    def nieuw_goed(self, categorie, merk, type, date=datetime.datetime.utcnow()):
        nieuw_goed = Goed(zaak_id=self._zaak_id, categorie=categorie, merk=merk, type=type, created_date=date)
        nieuw_goed.save_to_mongo()

    # def get_goederen(self):
    #     return Goed.from_zaak(self._zaak_id)

    def save_to_db(self):
        Database.insert(collection='cases', data=self.json())

    def json(self):
        return{
                    'verbalisant_id': self.verbalisant_id,
                    'verbalisant': self.verbalisant,
                    'zaaknaam': self.zaaknaam,
                    'bvh_nummer': self.bvh_nummer,
                    'omschrijving': self.omschrijving,
                    '_zaak_id': self._zaak_id
        }

    @classmethod
    def from_mongo(cls, _zaak_id):
        zaak_data = Database.find_one(collection='cases',
                                                      query={'_zaak_id': _zaak_id})
        return cls(**zaak_data)

    @classmethod
    def find_by_verbalisant_id(cls, verbalisant_id):
        zaken = Database.find(collection='cases', query={'verbalisant_id': verbalisant_id})
        return [cls(**zaak) for zaak in zaken]