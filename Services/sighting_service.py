from Data.repo import Repo
from Data.models import *
from typing import List

# this class contains calls that deal with sightings

class SightingService:
    def __init__(self):
        self.repo = Repo()
    
    def get_all_sightings(self) -> List[Sighting]:
        return self.repo.get_all_sightings()

    def get_sightings_paginated(self, page: int) -> List[Sighting]:
        return self.repo.get_sightings_paginated(page)

    def add_sighting(date, location, description, witness):
        self.repo.add_sighting(date, location, description, witness)
