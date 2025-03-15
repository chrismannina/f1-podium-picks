import asyncio
import logging
from datetime import datetime
from sqlalchemy.orm import Session
from typing import Dict, List, Any, Optional

from app.db import models, schemas, crud
from app.core import f1_api

logger = logging.getLogger(__name__)


async def parse_date(date_str: str) -> Optional[datetime.date]:
    """Parse a date string to a Python date object."""
    if not date_str:
        return None
        
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        logger.error(f"Failed to parse date: {date_str}")
        return None


async def import_seasons(db: Session, start_year: int = 1950, end_year: int = None) -> int:
    """Import F1 seasons into the database.
    
    Args:
        db: Database session
        start_year: Year to start importing from (default: 1950)
        end_year: Year to end importing at (default: current year)
        
    Returns:
        Number of seasons imported
    """
    if not end_year:
        end_year = datetime.now().year
        
    seasons_data = await f1_api.fetch_seasons()
    count = 0
    
    for season_data in seasons_data:
        season_year = int(season_data["season"])
        
        # Skip seasons outside our specified range
        if season_year < start_year or season_year > end_year:
            continue
            
        # Check if season already exists
        existing_season = crud.get_season_by_year(db, season_year)
        if existing_season:
            logger.info(f"Season {season_year} already exists, skipping")
            continue
            
        # Create new season
        season_create = schemas.SeasonCreate(
            year=season_year,
            wikipedia=season_data.get("url", None)
        )
        
        crud.create_season(db, season_create)
        count += 1
        
    logger.info(f"Imported {count} seasons")
    return count


async def import_circuits(db: Session) -> int:
    """Import all F1 circuits into the database.
    
    Args:
        db: Database session
        
    Returns:
        Number of circuits imported
    """
    circuits_data = await f1_api.fetch_circuits()
    count = 0
    
    for circuit_data in circuits_data:
        circuit_reference = circuit_data["circuitId"]
        
        # Check if circuit already exists
        existing_circuit = crud.get_circuit_by_reference(db, circuit_reference)
        if existing_circuit:
            logger.info(f"Circuit {circuit_reference} already exists, skipping")
            continue
            
        # Extract location data
        location = circuit_data.get("Location", {})
        
        # Create new circuit
        circuit_create = schemas.CircuitCreate(
            reference=circuit_reference,
            name=circuit_data["circuitName"],
            locality=location.get("locality", None),
            country=location.get("country", None),
            country_code=None,  # Not provided by API
            latitude=float(location.get("lat", 0)) if location.get("lat") else None,
            longitude=float(location.get("long", 0)) if location.get("long") else None,
            altitude=None,  # Not provided by API
            wikipedia=circuit_data.get("url", None)
        )
        
        crud.create_circuit(db, circuit_create)
        count += 1
        
    logger.info(f"Imported {count} circuits")
    return count


async def import_drivers(db: Session) -> int:
    """Import all F1 drivers into the database.
    
    Args:
        db: Database session
        
    Returns:
        Number of drivers imported
    """
    drivers_data = await f1_api.fetch_drivers()
    count = 0
    
    for driver_data in drivers_data:
        driver_reference = driver_data["driverId"]
        
        # Check if driver already exists
        existing_driver = crud.get_driver_by_reference(db, driver_reference)
        if existing_driver:
            logger.info(f"Driver {driver_reference} already exists, skipping")
            continue
            
        # Create new driver
        driver_create = schemas.DriverCreate(
            reference=driver_reference,
            forename=driver_data["givenName"],
            surname=driver_data["familyName"],
            abbreviation=driver_data.get("code", None),
            nationality=driver_data.get("nationality", None),
            country_code=None,  # Not provided by API
            permanent_car_number=int(driver_data["permanentNumber"]) if "permanentNumber" in driver_data else None,
            date_of_birth=await parse_date(driver_data.get("dateOfBirth", None)),
            wikipedia=driver_data.get("url", None)
        )
        
        crud.create_driver(db, driver_create)
        count += 1
        
    logger.info(f"Imported {count} drivers")
    return count


async def import_teams(db: Session) -> int:
    """Import all F1 teams (constructors) into the database.
    
    Args:
        db: Database session
        
    Returns:
        Number of teams imported
    """
    constructors_data = await f1_api.fetch_constructors()
    count = 0
    
    for constructor_data in constructors_data:
        constructor_reference = constructor_data["constructorId"]
        
        # Check if team already exists
        existing_team = crud.get_team_by_reference(db, constructor_reference)
        if existing_team:
            logger.info(f"Team {constructor_reference} already exists, skipping")
            continue
            
        # Create new team
        team_create = schemas.TeamCreate(
            reference=constructor_reference,
            name=constructor_data["name"],
            nationality=constructor_data.get("nationality", None),
            country_code=None,  # Not provided by API
            constructor_id=constructor_reference,
            wikipedia=constructor_data.get("url", None)
        )
        
        crud.create_team(db, team_create)
        count += 1
        
    logger.info(f"Imported {count} teams")
    return count


async def import_rounds_for_season(db: Session, season_year: int) -> int:
    """Import all rounds (races) for a specific season.
    
    Args:
        db: Database session
        season_year: Year of the season to import
        
    Returns:
        Number of rounds imported
    """
    # Get season
    season = crud.get_season_by_year(db, season_year)
    if not season:
        logger.error(f"Season {season_year} not found")
        return 0
        
    races_data = await f1_api.fetch_races(season_year)
    count = 0
    
    for race_data in races_data:
        # Get or create circuit
        circuit_reference = race_data["Circuit"]["circuitId"]
        circuit = crud.get_circuit_by_reference(db, circuit_reference)
        
        if not circuit:
            # Circuit doesn't exist, create it
            location = race_data["Circuit"].get("Location", {})
            
            circuit_create = schemas.CircuitCreate(
                reference=circuit_reference,
                name=race_data["Circuit"]["circuitName"],
                locality=location.get("locality", None),
                country=location.get("country", None),
                country_code=None,
                latitude=float(location.get("lat", 0)) if location.get("lat") else None,
                longitude=float(location.get("long", 0)) if location.get("long") else None,
                altitude=None,
                wikipedia=race_data["Circuit"].get("url", None)
            )
            
            circuit = crud.create_circuit(db, circuit_create)
        
        # Create round
        round_reference = f"{season_year}-{race_data['round']}"
        
        # Check if round already exists
        existing_round = crud.get_round_by_reference(db, round_reference)
        if existing_round:
            logger.info(f"Round {round_reference} already exists, skipping")
            continue
            
        round_create = schemas.RoundCreate(
            reference=round_reference,
            name=race_data["raceName"],
            round_number=int(race_data["round"]),
            date=await parse_date(race_data.get("date", None)),
            time=race_data.get("time", None),
            wikipedia=race_data.get("url", None),
            season_id=season.id,
            circuit_id=circuit.id
        )
        
        round_obj = crud.create_round(db, round_create)
        count += 1
        
        # Create sessions for this round
        await import_sessions_for_round(db, season_year, int(race_data["round"]), round_obj.id)
        
    logger.info(f"Imported {count} rounds for season {season_year}")
    return count


async def import_sessions_for_round(db: Session, season_year: int, round_num: int, round_id: int) -> int:
    """Import all sessions for a specific round.
    
    Args:
        db: Database session
        season_year: Year of the season
        round_num: Round number
        round_id: Database ID of the round
        
    Returns:
        Number of sessions imported
    """
    count = 0
    race_data = await f1_api.fetch_races(season_year)
    
    # Find the specific race data for this round
    race_info = None
    for race in race_data:
        if int(race["round"]) == round_num:
            race_info = race
            break
            
    if not race_info:
        logger.error(f"Race data not found for season {season_year}, round {round_num}")
        return 0
    
    # Create race session
    race_session_create = schemas.SessionCreate(
        session_type="race",
        date=await parse_date(race_info.get("date", None)),
        time=race_info.get("time", None),
        status="completed",  # Assume completed for historical data
        round_id=round_id
    )
    
    crud.create_session(db, race_session_create)
    count += 1
    
    # Check for qualifying
    quali_data = await f1_api.fetch_qualifying_results(season_year, round_num)
    if quali_data:
        quali_session_create = schemas.SessionCreate(
            session_type="qualifying",
            date=await parse_date(race_info.get("Qualifying", {}).get("date", race_info.get("date", None))),
            time=race_info.get("Qualifying", {}).get("time", None),
            status="completed",
            round_id=round_id
        )
        
        crud.create_session(db, quali_session_create)
        count += 1
    
    # Check for sprint
    sprint_data = await f1_api.fetch_sprint_results(season_year, round_num)
    if sprint_data:
        sprint_session_create = schemas.SessionCreate(
            session_type="sprint",
            date=await parse_date(race_info.get("Sprint", {}).get("date", race_info.get("date", None))),
            time=race_info.get("Sprint", {}).get("time", None),
            status="completed",
            round_id=round_id
        )
        
        crud.create_session(db, sprint_session_create)
        count += 1
    
    # Add practice sessions based on era
    # Modern F1 has three practice sessions, older eras might have had different formats
    if season_year >= 2000:  # Modern era assumption
        # Practice 1
        p1_session_create = schemas.SessionCreate(
            session_type="practice1",
            date=await parse_date(race_info.get("FirstPractice", {}).get("date", None)),
            time=race_info.get("FirstPractice", {}).get("time", None),
            status="completed",
            round_id=round_id
        )
        
        crud.create_session(db, p1_session_create)
        count += 1
        
        # Practice 2
        p2_session_create = schemas.SessionCreate(
            session_type="practice2",
            date=await parse_date(race_info.get("SecondPractice", {}).get("date", None)),
            time=race_info.get("SecondPractice", {}).get("time", None),
            status="completed",
            round_id=round_id
        )
        
        crud.create_session(db, p2_session_create)
        count += 1
        
        # Practice 3 (if not a sprint weekend)
        if not sprint_data and "ThirdPractice" in race_info:
            p3_session_create = schemas.SessionCreate(
                session_type="practice3",
                date=await parse_date(race_info.get("ThirdPractice", {}).get("date", None)),
                time=race_info.get("ThirdPractice", {}).get("time", None),
                status="completed",
                round_id=round_id
            )
            
            crud.create_session(db, p3_session_create)
            count += 1
    
    logger.info(f"Imported {count} sessions for round {round_num} of season {season_year}")
    return count


async def import_team_drivers_for_season(db: Session, season_year: int) -> int:
    """Import all team-driver pairings for a specific season.
    
    Args:
        db: Database session
        season_year: Year of the season
        
    Returns:
        Number of team-driver pairings imported
    """
    team_drivers_data = await f1_api.fetch_driver_constructor_by_season(season_year)
    count = 0
    
    for team_driver_data in team_drivers_data:
        driver_reference = team_driver_data["driverId"]
        team_reference = team_driver_data["constructorId"]
        
        # Get driver and team
        driver = crud.get_driver_by_reference(db, driver_reference)
        team = crud.get_team_by_reference(db, team_reference)
        
        if not driver or not team:
            logger.error(f"Driver {driver_reference} or team {team_reference} not found")
            continue
            
        # Check if team-driver pairing already exists
        existing = db.query(models.TeamDriver).filter(
            models.TeamDriver.team_id == team.id,
            models.TeamDriver.driver_id == driver.id,
            models.TeamDriver.season_year == season_year
        ).first()
        
        if existing:
            logger.info(f"Team-driver pairing {team_reference}-{driver_reference} for {season_year} already exists")
            continue
            
        # Create new team-driver pairing
        team_driver_create = schemas.TeamDriverCreate(
            team_id=team.id,
            driver_id=driver.id,
            season_year=season_year
        )
        
        crud.create_team_driver(db, team_driver_create)
        count += 1
        
    logger.info(f"Imported {count} team-driver pairings for season {season_year}")
    return count


async def import_all_f1_data(db: Session, start_year: int = 2020, end_year: int = None) -> Dict[str, int]:
    """Import all F1 data for the specified range of seasons.
    
    Args:
        db: Database session
        start_year: Year to start importing from (default: 2020)
        end_year: Year to end importing at (default: current year)
        
    Returns:
        Dictionary with counts of imported items by category
    """
    if not end_year:
        end_year = datetime.now().year
        
    results = {}
    
    # Import base data
    results["seasons"] = await import_seasons(db, start_year, end_year)
    results["circuits"] = await import_circuits(db)
    results["drivers"] = await import_drivers(db)
    results["teams"] = await import_teams(db)
    
    # Import season-specific data for each year in range
    results["rounds"] = 0
    results["team_drivers"] = 0
    
    for year in range(start_year, end_year + 1):
        results["rounds"] += await import_rounds_for_season(db, year)
        results["team_drivers"] += await import_team_drivers_for_season(db, year)
    
    return results 