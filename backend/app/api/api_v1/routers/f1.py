from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, Query
from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional
import logging

from app.db.session import get_db
from app.db import schemas, crud
from app.core import data_import

logger = logging.getLogger(__name__)

f1_router = APIRouter()


@f1_router.get("/circuits", response_model=List[schemas.Circuit])
async def get_circuits(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all circuits."""
    return crud.get_circuits(db, skip=skip, limit=limit)


@f1_router.get("/circuits/{circuit_id}", response_model=schemas.Circuit)
async def get_circuit(
    circuit_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific circuit by ID."""
    return crud.get_circuit(db, circuit_id=circuit_id)


@f1_router.get("/drivers", response_model=List[schemas.Driver])
async def get_drivers(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all drivers."""
    return crud.get_drivers(db, skip=skip, limit=limit)


@f1_router.get("/drivers/{driver_id}", response_model=schemas.Driver)
async def get_driver(
    driver_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific driver by ID."""
    return crud.get_driver(db, driver_id=driver_id)


@f1_router.get("/teams", response_model=List[schemas.Team])
async def get_teams(
    skip: int = 0, 
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all teams."""
    return crud.get_teams(db, skip=skip, limit=limit)


@f1_router.get("/teams/{team_id}", response_model=schemas.Team)
async def get_team(
    team_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific team by ID."""
    return crud.get_team(db, team_id=team_id)


@f1_router.get("/seasons", response_model=List[schemas.Season])
async def get_seasons(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all seasons."""
    return crud.get_seasons(db, skip=skip, limit=limit)


@f1_router.get("/seasons/{season_id}", response_model=schemas.Season)
async def get_season(
    season_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific season by ID."""
    return crud.get_season(db, season_id=season_id)


@f1_router.get("/seasons/year/{year}", response_model=schemas.Season)
async def get_season_by_year(
    year: int,
    db: Session = Depends(get_db)
):
    """Get a specific season by year."""
    season = crud.get_season_by_year(db, year=year)
    if not season:
        raise HTTPException(status_code=404, detail=f"Season for year {year} not found")
    return season


@f1_router.get("/rounds", response_model=List[schemas.Round])
async def get_rounds(
    skip: int = 0,
    limit: int = 100,
    season_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """Get all rounds, optionally filtered by season."""
    if season_id:
        return crud.get_rounds_by_season(db, season_id=season_id)
    return crud.get_rounds(db, skip=skip, limit=limit)


@f1_router.get("/rounds/{round_id}", response_model=schemas.Round)
async def get_round(
    round_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific round by ID."""
    return crud.get_round(db, round_id=round_id)


@f1_router.get("/sessions", response_model=List[schemas.Session])
async def get_sessions(
    skip: int = 0,
    limit: int = 100,
    round_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """Get all sessions, optionally filtered by round."""
    if round_id:
        return crud.get_sessions_by_round(db, round_id=round_id)
    return crud.get_sessions(db, skip=skip, limit=limit)


@f1_router.get("/sessions/{session_id}", response_model=schemas.Session)
async def get_session(
    session_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific session by ID."""
    return crud.get_session(db, session_id=session_id)


@f1_router.get("/teamdrivers", response_model=List[schemas.TeamDriver])
async def get_team_drivers(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all team-driver pairings."""
    return crud.get_team_drivers(db, skip=skip, limit=limit)


@f1_router.get("/results", response_model=List[schemas.Result])
async def get_results(
    skip: int = 0,
    limit: int = 100,
    session_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """Get all results, optionally filtered by session."""
    if session_id:
        return crud.get_results_by_session(db, session_id=session_id)
    return crud.get_results(db, skip=skip, limit=limit)


@f1_router.get("/import/status")
async def get_import_status():
    """Get the status of the data import process."""
    # In a real application, you would track the import status in a database or cache
    return {"status": "No import in progress"}


@f1_router.post("/import/all")
async def import_all_data(
    background_tasks: BackgroundTasks,
    start_year: int = Query(2020, description="The year to start importing data from"),
    end_year: Optional[int] = Query(None, description="The year to end importing data at (default: current year)"),
    db: Session = Depends(get_db)
):
    """Import all F1 data in the background."""
    # Add the import task to background tasks
    background_tasks.add_task(data_import.import_all_f1_data, db, start_year, end_year)
    
    return {
        "message": f"Data import started for years {start_year} to {end_year or 'current'}. This may take several minutes.",
        "status": "in_progress"
    }


@f1_router.post("/import/seasons")
async def import_seasons(
    background_tasks: BackgroundTasks,
    start_year: int = Query(1950, description="The year to start importing seasons from"),
    end_year: Optional[int] = Query(None, description="The year to end importing seasons at"),
    db: Session = Depends(get_db)
):
    """Import F1 seasons in the background."""
    background_tasks.add_task(data_import.import_seasons, db, start_year, end_year)
    
    return {
        "message": f"Season import started for years {start_year} to {end_year or 'current'}",
        "status": "in_progress"
    }


@f1_router.post("/import/circuits")
async def import_circuits(
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Import all F1 circuits in the background."""
    background_tasks.add_task(data_import.import_circuits, db)
    
    return {
        "message": "Circuit import started",
        "status": "in_progress"
    }


@f1_router.post("/import/drivers")
async def import_drivers(
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Import all F1 drivers in the background."""
    background_tasks.add_task(data_import.import_drivers, db)
    
    return {
        "message": "Driver import started",
        "status": "in_progress"
    }


@f1_router.post("/import/teams")
async def import_teams(
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Import all F1 teams in the background."""
    background_tasks.add_task(data_import.import_teams, db)
    
    return {
        "message": "Team import started",
        "status": "in_progress"
    }


@f1_router.post("/import/rounds/{season_year}")
async def import_rounds_for_season(
    season_year: int,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Import all rounds for a specific season in the background."""
    background_tasks.add_task(data_import.import_rounds_for_season, db, season_year)
    
    return {
        "message": f"Round import started for season {season_year}",
        "status": "in_progress"
    }


@f1_router.post("/import/teamdrivers/{season_year}")
async def import_team_drivers_for_season(
    season_year: int,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Import all team-driver pairings for a specific season in the background."""
    background_tasks.add_task(data_import.import_team_drivers_for_season, db, season_year)
    
    return {
        "message": f"Team-driver import started for season {season_year}",
        "status": "in_progress"
    } 