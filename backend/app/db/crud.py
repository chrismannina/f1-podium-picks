from fastapi import HTTPException, status
from sqlalchemy.orm import Session
import typing as t

from . import models, schemas
from app.core.security import get_password_hash


def get_user(db: Session, user_id: int):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def get_user_by_email(db: Session, email: str) -> schemas.UserBase:
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(
    db: Session, skip: int = 0, limit: int = 100
) -> t.List[schemas.UserOut]:
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        hashed_password=hashed_password,
        is_active=user.is_active,
        is_superuser=user.is_superuser,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int):
    user = get_user(db, user_id)
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="User not found")
    db.delete(user)
    db.commit()
    return user


def edit_user(
    db: Session, user_id: int, user: schemas.UserEdit
) -> schemas.User:
    db_user = get_user(db, user_id)
    if not db_user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="User not found")
    update_data = user.dict(exclude_unset=True)

    if "password" in update_data:
        update_data["hashed_password"] = get_password_hash(user.password)
        del update_data["password"]

    for key, value in update_data.items():
        setattr(db_user, key, value)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# Circuit CRUD operations
def get_circuit(db: Session, circuit_id: int) -> schemas.Circuit:
    circuit = db.query(models.Circuit).filter(models.Circuit.id == circuit_id).first()
    if not circuit:
        raise HTTPException(status_code=404, detail="Circuit not found")
    return circuit


def get_circuit_by_reference(db: Session, reference: str) -> schemas.Circuit:
    return db.query(models.Circuit).filter(models.Circuit.reference == reference).first()


def get_circuits(db: Session, skip: int = 0, limit: int = 100) -> t.List[schemas.Circuit]:
    return db.query(models.Circuit).offset(skip).limit(limit).all()


def create_circuit(db: Session, circuit: schemas.CircuitCreate) -> schemas.Circuit:
    db_circuit = models.Circuit(**circuit.dict())
    db.add(db_circuit)
    db.commit()
    db.refresh(db_circuit)
    return db_circuit


def update_circuit(db: Session, circuit_id: int, circuit: schemas.CircuitUpdate) -> schemas.Circuit:
    db_circuit = get_circuit(db, circuit_id)
    update_data = circuit.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_circuit, key, value)
    db.add(db_circuit)
    db.commit()
    db.refresh(db_circuit)
    return db_circuit


def delete_circuit(db: Session, circuit_id: int) -> schemas.Circuit:
    db_circuit = get_circuit(db, circuit_id)
    db.delete(db_circuit)
    db.commit()
    return db_circuit


# Driver CRUD operations
def get_driver(db: Session, driver_id: int) -> schemas.Driver:
    driver = db.query(models.Driver).filter(models.Driver.id == driver_id).first()
    if not driver:
        raise HTTPException(status_code=404, detail="Driver not found")
    return driver


def get_driver_by_reference(db: Session, reference: str) -> schemas.Driver:
    return db.query(models.Driver).filter(models.Driver.reference == reference).first()


def get_drivers(db: Session, skip: int = 0, limit: int = 100) -> t.List[schemas.Driver]:
    return db.query(models.Driver).offset(skip).limit(limit).all()


def create_driver(db: Session, driver: schemas.DriverCreate) -> schemas.Driver:
    db_driver = models.Driver(**driver.dict())
    db.add(db_driver)
    db.commit()
    db.refresh(db_driver)
    return db_driver


def update_driver(db: Session, driver_id: int, driver: schemas.DriverUpdate) -> schemas.Driver:
    db_driver = get_driver(db, driver_id)
    update_data = driver.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_driver, key, value)
    db.add(db_driver)
    db.commit()
    db.refresh(db_driver)
    return db_driver


def delete_driver(db: Session, driver_id: int) -> schemas.Driver:
    db_driver = get_driver(db, driver_id)
    db.delete(db_driver)
    db.commit()
    return db_driver


# Team CRUD operations
def get_team(db: Session, team_id: int) -> schemas.Team:
    team = db.query(models.Team).filter(models.Team.id == team_id).first()
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    return team


def get_team_by_reference(db: Session, reference: str) -> schemas.Team:
    return db.query(models.Team).filter(models.Team.reference == reference).first()


def get_teams(db: Session, skip: int = 0, limit: int = 100) -> t.List[schemas.Team]:
    return db.query(models.Team).offset(skip).limit(limit).all()


def create_team(db: Session, team: schemas.TeamCreate) -> schemas.Team:
    db_team = models.Team(**team.dict())
    db.add(db_team)
    db.commit()
    db.refresh(db_team)
    return db_team


def update_team(db: Session, team_id: int, team: schemas.TeamUpdate) -> schemas.Team:
    db_team = get_team(db, team_id)
    update_data = team.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_team, key, value)
    db.add(db_team)
    db.commit()
    db.refresh(db_team)
    return db_team


def delete_team(db: Session, team_id: int) -> schemas.Team:
    db_team = get_team(db, team_id)
    db.delete(db_team)
    db.commit()
    return db_team


# Season CRUD operations
def get_season(db: Session, season_id: int) -> schemas.Season:
    season = db.query(models.Season).filter(models.Season.id == season_id).first()
    if not season:
        raise HTTPException(status_code=404, detail="Season not found")
    return season


def get_season_by_year(db: Session, year: int) -> schemas.Season:
    return db.query(models.Season).filter(models.Season.year == year).first()


def get_seasons(db: Session, skip: int = 0, limit: int = 100) -> t.List[schemas.Season]:
    return db.query(models.Season).offset(skip).limit(limit).all()


def create_season(db: Session, season: schemas.SeasonCreate) -> schemas.Season:
    db_season = models.Season(**season.dict())
    db.add(db_season)
    db.commit()
    db.refresh(db_season)
    return db_season


def update_season(db: Session, season_id: int, season: schemas.SeasonUpdate) -> schemas.Season:
    db_season = get_season(db, season_id)
    update_data = season.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_season, key, value)
    db.add(db_season)
    db.commit()
    db.refresh(db_season)
    return db_season


def delete_season(db: Session, season_id: int) -> schemas.Season:
    db_season = get_season(db, season_id)
    db.delete(db_season)
    db.commit()
    return db_season


# Round CRUD operations
def get_round(db: Session, round_id: int) -> schemas.Round:
    round_obj = db.query(models.Round).filter(models.Round.id == round_id).first()
    if not round_obj:
        raise HTTPException(status_code=404, detail="Round not found")
    return round_obj


def get_round_by_reference(db: Session, reference: str) -> schemas.Round:
    return db.query(models.Round).filter(models.Round.reference == reference).first()


def get_rounds(db: Session, skip: int = 0, limit: int = 100) -> t.List[schemas.Round]:
    return db.query(models.Round).offset(skip).limit(limit).all()


def get_rounds_by_season(db: Session, season_id: int) -> t.List[schemas.Round]:
    return db.query(models.Round).filter(models.Round.season_id == season_id).all()


def create_round(db: Session, round_obj: schemas.RoundCreate) -> schemas.Round:
    db_round = models.Round(**round_obj.dict())
    db.add(db_round)
    db.commit()
    db.refresh(db_round)
    return db_round


def update_round(db: Session, round_id: int, round_obj: schemas.RoundUpdate) -> schemas.Round:
    db_round = get_round(db, round_id)
    update_data = round_obj.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_round, key, value)
    db.add(db_round)
    db.commit()
    db.refresh(db_round)
    return db_round


def delete_round(db: Session, round_id: int) -> schemas.Round:
    db_round = get_round(db, round_id)
    db.delete(db_round)
    db.commit()
    return db_round


# Session CRUD operations
def get_session(db: Session, session_id: int) -> schemas.Session:
    session = db.query(models.Session).filter(models.Session.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session


def get_sessions(db: Session, skip: int = 0, limit: int = 100) -> t.List[schemas.Session]:
    return db.query(models.Session).offset(skip).limit(limit).all()


def get_sessions_by_round(db: Session, round_id: int) -> t.List[schemas.Session]:
    return db.query(models.Session).filter(models.Session.round_id == round_id).all()


def create_session(db: Session, session: schemas.SessionCreate) -> schemas.Session:
    db_session = models.Session(**session.dict())
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return db_session


def update_session(db: Session, session_id: int, session: schemas.SessionUpdate) -> schemas.Session:
    db_session = get_session(db, session_id)
    update_data = session.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_session, key, value)
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return db_session


def delete_session(db: Session, session_id: int) -> schemas.Session:
    db_session = get_session(db, session_id)
    db.delete(db_session)
    db.commit()
    return db_session


# Team Driver CRUD operations
def get_team_driver(db: Session, team_driver_id: int) -> schemas.TeamDriver:
    team_driver = db.query(models.TeamDriver).filter(models.TeamDriver.id == team_driver_id).first()
    if not team_driver:
        raise HTTPException(status_code=404, detail="Team Driver relationship not found")
    return team_driver


def get_team_drivers(db: Session, skip: int = 0, limit: int = 100) -> t.List[schemas.TeamDriver]:
    return db.query(models.TeamDriver).offset(skip).limit(limit).all()


def create_team_driver(db: Session, team_driver: schemas.TeamDriverCreate) -> schemas.TeamDriver:
    db_team_driver = models.TeamDriver(**team_driver.dict())
    db.add(db_team_driver)
    db.commit()
    db.refresh(db_team_driver)
    return db_team_driver


def delete_team_driver(db: Session, team_driver_id: int) -> schemas.TeamDriver:
    db_team_driver = get_team_driver(db, team_driver_id)
    db.delete(db_team_driver)
    db.commit()
    return db_team_driver


# Result CRUD operations
def get_result(db: Session, result_id: int) -> schemas.Result:
    result = db.query(models.Result).filter(models.Result.id == result_id).first()
    if not result:
        raise HTTPException(status_code=404, detail="Result not found")
    return result


def get_results(db: Session, skip: int = 0, limit: int = 100) -> t.List[schemas.Result]:
    return db.query(models.Result).offset(skip).limit(limit).all()


def get_results_by_session(db: Session, session_id: int) -> t.List[schemas.Result]:
    return db.query(models.Result).filter(models.Result.session_id == session_id).all()


def create_result(db: Session, result: schemas.ResultCreate) -> schemas.Result:
    db_result = models.Result(**result.dict())
    db.add(db_result)
    db.commit()
    db.refresh(db_result)
    return db_result


def update_result(db: Session, result_id: int, result: schemas.ResultUpdate) -> schemas.Result:
    db_result = get_result(db, result_id)
    update_data = result.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_result, key, value)
    db.add(db_result)
    db.commit()
    db.refresh(db_result)
    return db_result


def delete_result(db: Session, result_id: int) -> schemas.Result:
    db_result = get_result(db, result_id)
    db.delete(db_result)
    db.commit()
    return db_result
