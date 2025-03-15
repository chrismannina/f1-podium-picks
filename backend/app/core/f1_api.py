import aiohttp
import asyncio
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

BASE_URL = "http://api.jolpi.ca/ergast/f1"


async def fetch_data(session: aiohttp.ClientSession, url: str) -> Dict[str, Any]:
    """Generic function to fetch data from the Ergast API."""
    try:
        async with session.get(url) as response:
            if response.status != 200:
                logger.error(f"Error fetching data from {url}: {response.status}")
                return {"error": f"HTTP error {response.status}"}
            
            data = await response.json()
            return data
    except Exception as e:
        logger.error(f"Exception when fetching data from {url}: {str(e)}")
        return {"error": str(e)}


async def fetch_seasons() -> List[Dict[str, Any]]:
    """Fetch all F1 seasons from the Ergast API."""
    async with aiohttp.ClientSession() as session:
        url = f"{BASE_URL}/seasons.json?limit=100"
        data = await fetch_data(session, url)
        
        if "error" in data:
            return []
        
        try:
            seasons = data["MRData"]["SeasonTable"]["Seasons"]
            return seasons
        except KeyError as e:
            logger.error(f"Key error when parsing seasons data: {str(e)}")
            return []


async def fetch_drivers(season: Optional[int] = None) -> List[Dict[str, Any]]:
    """Fetch all F1 drivers, optionally filtered by season."""
    async with aiohttp.ClientSession() as session:
        base_url = f"{BASE_URL}"
        if season:
            url = f"{base_url}/{season}/drivers.json?limit=100"
        else:
            url = f"{base_url}/drivers.json?limit=1000"
            
        data = await fetch_data(session, url)
        
        if "error" in data:
            return []
        
        try:
            drivers = data["MRData"]["DriverTable"]["Drivers"]
            return drivers
        except KeyError as e:
            logger.error(f"Key error when parsing drivers data: {str(e)}")
            return []


async def fetch_constructors(season: Optional[int] = None) -> List[Dict[str, Any]]:
    """Fetch all F1 constructors/teams, optionally filtered by season."""
    async with aiohttp.ClientSession() as session:
        base_url = f"{BASE_URL}"
        if season:
            url = f"{base_url}/{season}/constructors.json?limit=100"
        else:
            url = f"{base_url}/constructors.json?limit=1000"
            
        data = await fetch_data(session, url)
        
        if "error" in data:
            return []
        
        try:
            constructors = data["MRData"]["ConstructorTable"]["Constructors"]
            return constructors
        except KeyError as e:
            logger.error(f"Key error when parsing constructors data: {str(e)}")
            return []


async def fetch_circuits(season: Optional[int] = None) -> List[Dict[str, Any]]:
    """Fetch all F1 circuits, optionally filtered by season."""
    async with aiohttp.ClientSession() as session:
        base_url = f"{BASE_URL}"
        if season:
            url = f"{base_url}/{season}/circuits.json?limit=100"
        else:
            url = f"{base_url}/circuits.json?limit=1000"
            
        data = await fetch_data(session, url)
        
        if "error" in data:
            return []
        
        try:
            circuits = data["MRData"]["CircuitTable"]["Circuits"]
            return circuits
        except KeyError as e:
            logger.error(f"Key error when parsing circuits data: {str(e)}")
            return []


async def fetch_races(season: int) -> List[Dict[str, Any]]:
    """Fetch all races for a given season."""
    async with aiohttp.ClientSession() as session:
        url = f"{BASE_URL}/{season}.json?limit=100"
        data = await fetch_data(session, url)
        
        if "error" in data:
            return []
        
        try:
            races = data["MRData"]["RaceTable"]["Races"]
            return races
        except KeyError as e:
            logger.error(f"Key error when parsing races data: {str(e)}")
            return []


async def fetch_race_results(season: int, round_num: int) -> List[Dict[str, Any]]:
    """Fetch results for a specific race."""
    async with aiohttp.ClientSession() as session:
        url = f"{BASE_URL}/{season}/{round_num}/results.json?limit=100"
        data = await fetch_data(session, url)
        
        if "error" in data:
            return []
        
        try:
            results = data["MRData"]["RaceTable"]["Races"][0]["Results"]
            return results
        except (KeyError, IndexError) as e:
            logger.error(f"Error when parsing race results data: {str(e)}")
            return []


async def fetch_qualifying_results(season: int, round_num: int) -> List[Dict[str, Any]]:
    """Fetch qualifying results for a specific race."""
    async with aiohttp.ClientSession() as session:
        url = f"{BASE_URL}/{season}/{round_num}/qualifying.json?limit=100"
        data = await fetch_data(session, url)
        
        if "error" in data:
            return []
        
        try:
            qualifying_results = data["MRData"]["RaceTable"]["Races"][0]["QualifyingResults"]
            return qualifying_results
        except (KeyError, IndexError) as e:
            logger.error(f"Error when parsing qualifying results data: {str(e)}")
            return []


async def fetch_sprint_results(season: int, round_num: int) -> List[Dict[str, Any]]:
    """Fetch sprint results for a specific race, if available."""
    async with aiohttp.ClientSession() as session:
        url = f"{BASE_URL}/{season}/{round_num}/sprint.json?limit=100"
        data = await fetch_data(session, url)
        
        if "error" in data:
            return []
        
        try:
            # Check if there are any races returned
            races = data["MRData"]["RaceTable"].get("Races", [])
            if not races:
                return []
                
            sprint_results = races[0]["SprintResults"]
            return sprint_results
        except (KeyError, IndexError) as e:
            logger.error(f"Error when parsing sprint results data: {str(e)}")
            return []


async def fetch_driver_standings(season: int, round_num: Optional[int] = None) -> List[Dict[str, Any]]:
    """Fetch driver standings for a given season, optionally after a specific round."""
    async with aiohttp.ClientSession() as session:
        if round_num:
            url = f"{BASE_URL}/{season}/{round_num}/driverStandings.json?limit=100"
        else:
            url = f"{BASE_URL}/{season}/driverStandings.json?limit=100"
            
        data = await fetch_data(session, url)
        
        if "error" in data:
            return []
        
        try:
            standings = data["MRData"]["StandingsTable"]["StandingsLists"][0]["DriverStandings"]
            return standings
        except (KeyError, IndexError) as e:
            logger.error(f"Error when parsing driver standings data: {str(e)}")
            return []


async def fetch_constructor_standings(season: int, round_num: Optional[int] = None) -> List[Dict[str, Any]]:
    """Fetch constructor standings for a given season, optionally after a specific round."""
    async with aiohttp.ClientSession() as session:
        if round_num:
            url = f"{BASE_URL}/{season}/{round_num}/constructorStandings.json?limit=100"
        else:
            url = f"{BASE_URL}/{season}/constructorStandings.json?limit=100"
            
        data = await fetch_data(session, url)
        
        if "error" in data:
            return []
        
        try:
            standings = data["MRData"]["StandingsTable"]["StandingsLists"][0]["ConstructorStandings"]
            return standings
        except (KeyError, IndexError) as e:
            logger.error(f"Error when parsing constructor standings data: {str(e)}")
            return []


async def fetch_driver_constructor_by_season(season: int) -> List[Dict[str, Any]]:
    """Fetch driver-constructor pairings for a given season."""
    async with aiohttp.ClientSession() as session:
        url = f"{BASE_URL}/{season}/driverStandings.json?limit=100"
        data = await fetch_data(session, url)
        
        if "error" in data:
            return []
        
        try:
            driver_standings = data["MRData"]["StandingsTable"]["StandingsLists"][0]["DriverStandings"]
            team_drivers = []
            
            for driver_standing in driver_standings:
                driver_id = driver_standing["Driver"]["driverId"]
                for constructor in driver_standing["Constructors"]:
                    team_drivers.append({
                        "driverId": driver_id,
                        "constructorId": constructor["constructorId"],
                        "season": season
                    })
            
            return team_drivers
        except (KeyError, IndexError) as e:
            logger.error(f"Error when parsing driver-constructor data: {str(e)}")
            return [] 