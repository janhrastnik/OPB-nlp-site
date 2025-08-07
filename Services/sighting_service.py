from Data.repo import Repo
from Data.models import *
from typing import List

# this class contains calls that deal with sightings

class SightingService:
    def __init__(self):
        self.repo = Repo()
    
    def get_all_sightings(self) -> List[Sighting]:
        return self.repo.get_all_sightings()
