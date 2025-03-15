from sqlalchemy import Boolean, Column, Integer, String, Float, Date, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from .session import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)


class Circuit(Base):
    __tablename__ = "circuit"

    id = Column(Integer, primary_key=True, index=True)
    reference = Column(String, unique=True, nullable=True, index=True)
    name = Column(String, nullable=False)
    locality = Column(String, nullable=True)
    country = Column(String, nullable=True)
    country_code = Column(String(3), nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    altitude = Column(Float, nullable=True)
    wikipedia = Column(String, nullable=True)
    
    # Relationships
    rounds = relationship("Round", back_populates="circuit")


class Driver(Base):
    __tablename__ = "driver"

    id = Column(Integer, primary_key=True, index=True)
    reference = Column(String, unique=True, nullable=True, index=True)
    forename = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    abbreviation = Column(String(10), nullable=True)
    nationality = Column(String, nullable=True)
    country_code = Column(String(3), nullable=True)
    permanent_car_number = Column(Integer, nullable=True)
    date_of_birth = Column(Date, nullable=True)
    wikipedia = Column(String, nullable=True)
    
    # Relationships
    team_drivers = relationship("TeamDriver", back_populates="driver")


class Team(Base):
    __tablename__ = "team"

    id = Column(Integer, primary_key=True, index=True)
    reference = Column(String, unique=True, nullable=True, index=True)
    name = Column(String, nullable=False)
    nationality = Column(String, nullable=True)
    country_code = Column(String(3), nullable=True)
    constructor_id = Column(String, nullable=True)
    wikipedia = Column(String, nullable=True)
    
    # Relationships
    team_drivers = relationship("TeamDriver", back_populates="team")


class Season(Base):
    __tablename__ = "season"

    id = Column(Integer, primary_key=True, index=True)
    year = Column(Integer, unique=True, nullable=False, index=True)
    wikipedia = Column(String, nullable=True)
    
    # Relationships
    rounds = relationship("Round", back_populates="season")


class Round(Base):
    __tablename__ = "round"

    id = Column(Integer, primary_key=True, index=True)
    reference = Column(String, unique=True, nullable=True, index=True)
    name = Column(String, nullable=False)
    round_number = Column(Integer, nullable=False)
    date = Column(Date, nullable=True)
    time = Column(String, nullable=True)
    wikipedia = Column(String, nullable=True)
    
    # Foreign keys
    season_id = Column(Integer, ForeignKey("season.id"), nullable=False)
    circuit_id = Column(Integer, ForeignKey("circuit.id"), nullable=False)
    
    # Relationships
    season = relationship("Season", back_populates="rounds")
    circuit = relationship("Circuit", back_populates="rounds")
    sessions = relationship("Session", back_populates="round")


class Session(Base):
    __tablename__ = "session"

    id = Column(Integer, primary_key=True, index=True)
    session_type = Column(String, nullable=False)  # race, qualifying, sprint, practice1, practice2, practice3
    date = Column(Date, nullable=True)
    time = Column(String, nullable=True)
    status = Column(String, nullable=True)
    
    # Foreign keys
    round_id = Column(Integer, ForeignKey("round.id"), nullable=False)
    
    # Relationships
    round = relationship("Round", back_populates="sessions")
    results = relationship("Result", back_populates="session")


class TeamDriver(Base):
    __tablename__ = "team_driver"

    id = Column(Integer, primary_key=True, index=True)
    season_year = Column(Integer, nullable=False)
    
    # Foreign keys
    team_id = Column(Integer, ForeignKey("team.id"), nullable=False)
    driver_id = Column(Integer, ForeignKey("driver.id"), nullable=False)
    
    # Relationships
    team = relationship("Team", back_populates="team_drivers")
    driver = relationship("Driver", back_populates="team_drivers")


class Result(Base):
    __tablename__ = "result"

    id = Column(Integer, primary_key=True, index=True)
    position = Column(Integer, nullable=True)
    position_text = Column(String, nullable=True)
    points = Column(Float, nullable=True)
    grid = Column(Integer, nullable=True)
    laps = Column(Integer, nullable=True)
    status = Column(String, nullable=True)
    time_millis = Column(Integer, nullable=True)
    fastest_lap = Column(Integer, nullable=True)
    fastest_lap_time = Column(String, nullable=True)
    
    # Foreign keys
    session_id = Column(Integer, ForeignKey("session.id"), nullable=False)
    driver_id = Column(Integer, ForeignKey("driver.id"), nullable=False)
    team_id = Column(Integer, ForeignKey("team.id"), nullable=False)
    
    # Relationships
    session = relationship("Session", back_populates="results")
    driver = relationship("Driver")
    team = relationship("Team")
