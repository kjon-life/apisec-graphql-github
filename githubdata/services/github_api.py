from typing import List, Optional, Dict, Any
import httpx
from datetime import datetime

class SpaceXAPI:
    BASE_URL = "https://api.spacexdata.com/v5"
    
    @staticmethod
    async def _make_request(endpoint: str, method: str = "GET", **kwargs) -> Dict[str, Any]:
        async with httpx.AsyncClient() as client:
            response = await client.request(
                method,
                f"{SpaceXAPI.BASE_URL}/{endpoint}",
                **kwargs
            )
            response.raise_for_status()
            return response.json()
    
    @staticmethod
    def _parse_launch(launch_data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "id": launch_data["id"],
            "name": launch_data["name"],
            "details": launch_data.get("details"),
            "date_utc": datetime.fromisoformat(launch_data["date_utc"].replace("Z", "+00:00")),
            "success": launch_data.get("success"),
            "flight_number": launch_data["flight_number"]
        }
    
    async def get_launch(self, launch_id: str) -> Optional[Dict[str, Any]]:
        try:
            data = await self._make_request(f"launches/{launch_id}")
            return self._parse_launch(data)
        except httpx.HTTPError:
            return None
    
    async def get_launches(self, limit: int = 10) -> List[Dict[str, Any]]:
        try:
            data = await self._make_request("launches/query", 
                method="POST",
                json={
                    "options": {
                        "limit": limit,
                        "sort": {
                            "date_utc": "desc"
                        }
                    }
                }
            )
            return [self._parse_launch(launch) for launch in data["docs"]]
        except httpx.HTTPError:
            return [] 