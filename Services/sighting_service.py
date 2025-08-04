from Data.repo import Repo

# this class contains calls that deal with sightings

class SightingService:
    def __init__(self):
        self.repo = Repo()
    
    def get_all_sightings(self):
        self.repo.get_all_sightings()
