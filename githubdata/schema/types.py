from typing import List, Optional
import strawberry
from datetime import datetime

@strawberry.type
class Launch:
    id: str
    name: str
    details: Optional[str]
    date_utc: datetime
    success: Optional[bool]
    flight_number: int

@strawberry.type
class Query:
    @strawberry.field
    async def launch(self, id: str) -> Optional[Launch]:
        """Get a specific launch by ID"""
        from ..resolvers.launch_resolver import LaunchResolver
        resolver = LaunchResolver()
        return await resolver.launch(id)

    @strawberry.field
    async def launches(self, limit: Optional[int] = 10) -> List[Launch]:
        """Get a list of launches"""
        from ..resolvers.launch_resolver import LaunchResolver
        resolver = LaunchResolver()
        return await resolver.launches(limit) 