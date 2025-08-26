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

    def get_user_sightings(self, email) -> List[Sighting]:
        user = self.repo.get_user(email)

        return self.repo.get_user_sightings(user.id)

    def get_sighting_by_id(self, sighting_id: int) -> Sighting:
        return self.repo.get_sighting_by_id(sighting_id)
    
    def add_sighting(self, email: str, user_timestamp: str, city: str, state: str, country: str, shape: str, duration_seconds: float, comment: str, latitude: float, langtitude: float) -> Sighting:
        # Generate title: "<Shape> sighting in <City>"
        title = f"Sighting of {shape}-shaped UFO in {city}, {country}"

        # Combine coords
        coords = f"{latitude},{langtitude}"

        # Combine duration nicely
        duration = f"{duration_seconds} seconds"

        # Parse user_timestamp into datetime
        sighting_date = datetime.strptime(user_timestamp, "%Y-%m-%d %H:%M:%S")

        # Set creation_date to now
        creation_date = datetime.now()

        # get the user that sent the add_sighting request
        user = self.repo.get_user(email)

        # Create Sighting object
        new_sighting = Sighting(
            title=title,
            sighting_date=sighting_date,
            description=comment,
            coords=coords,
            duration=duration,
            user_id=user.id,
            creation_date=creation_date
        )

        # Save to Repo
        self.repo.add_sighting(new_sighting)
        return new_sighting


    def delete_sighting(self, sighting_id: int, user_email: str) -> bool:
        user = self.repo.get_user(user_email)
        sighting = self.repo.get_sighting_by_id(sighting_id)
        if sighting and sighting.user_id == user.id:
            return self.repo.delete_sighting(sighting_id)
        return False

    def get_sighting_comments(self, sighting_id: int) -> List[CommentDto]:
        return self.repo.get_sighting_comments(sighting_id)

