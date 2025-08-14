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

    
    def add_sighting(self, user_timestamp: str, city: str, state: str, country: str, shape: str, duration_seconds: float, comment: str, latitude: float, langtitude: float, user_id: int = 1) -> Sighting:
        # Generate title: "<Shape> sighting in <City>"
        title = f"Sighting of {shape}-shaped UFO in {city}, {country}"

        # Combine coords
        coords = f"{latitude},{langtitude}"

        # Combine duration nicely
        duration = f"{duration_seconds}seconds"

        # Parse user_timestamp into datetime
        sighting_date = datetime.strptime(user_timestamp, "%Y-%m-%d %H:%M:%S")

        # Set creation_date to now
        creation_date = datetime.now()

        # Create Sighting object
        new_sighting = Sighting(
            title=title,
            sighting_date=sighting_date,
            description=comment,
            coords=coords,
            duration=duration,
            user_id=user_id,
            creation_date=creation_date
        )

        # Save to Repo
        self.repo.add_sighting(new_sighting)
        return new_sighting