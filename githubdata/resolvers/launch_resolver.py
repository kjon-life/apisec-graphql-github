from typing import List, Optional
from ..schema.types import Launch
from ..services.spacex_api import SpaceXAPI

class LaunchResolver:
    def __init__(self):
        self.spacex_api = SpaceXAPI()

    async def launch(self, id: str) -> Optional[Launch]:
        """Get a specific launch by ID"""
        data = await self.spacex_api.get_launch(id)
        if data:
            return Launch(**data)
        return None

    async def launches(self, limit: Optional[int] = 10) -> List[Launch]:
        """Get a list of launches"""
        data = await self.spacex_api.get_launches(limit or 10)
        return [Launch(**launch) for launch in data] 