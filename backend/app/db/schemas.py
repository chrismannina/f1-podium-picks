from pydantic import BaseModel
import typing as t
from datetime import date, datetime


class UserBase(BaseModel):
    email: str
    is_active: bool = True
    is_superuser: bool = False
    first_name: str = None
    last_name: str = None


class UserOut(UserBase):
    pass


class UserCreate(UserBase):
    password: str

    class Config:
        orm_mode = True


class UserEdit(UserBase):
    password: t.Optional[str] = None

    class Config:
        orm_mode = True


class User(UserBase):
    id: int

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str = None
    permissions: str = "user"


# F1 Schemas
class CircuitBase(BaseModel):
    reference: t.Optional[str] = None
    name: str
    locality: t.Optional[str] = None
    country: t.Optional[str] = None
    country_code: t.Optional[str] = None
    latitude: t.Optional[float] = None
    longitude: t.Optional[float] = None
    altitude: t.Optional[float] = None
    wikipedia: t.Optional[str] = None


class CircuitCreate(CircuitBase):
    pass


class CircuitUpdate(CircuitBase):
    pass


class Circuit(CircuitBase):
    id: int

    class Config:
        orm_mode = True


class DriverBase(BaseModel):
    reference: t.Optional[str] = None
    forename: str
    surname: str
    abbreviation: t.Optional[str] = None
    nationality: t.Optional[str] = None
    country_code: t.Optional[str] = None
    permanent_car_number: t.Optional[int] = None
    date_of_birth: t.Optional[date] = None
    wikipedia: t.Optional[str] = None


class DriverCreate(DriverBase):
    pass


class DriverUpdate(DriverBase):
    pass


class Driver(DriverBase):
    id: int

    class Config:
        orm_mode = True


class TeamBase(BaseModel):
    reference: t.Optional[str] = None
    name: str
    nationality: t.Optional[str] = None
    country_code: t.Optional[str] = None
    constructor_id: t.Optional[str] = None
    wikipedia: t.Optional[str] = None


class TeamCreate(TeamBase):
    pass


class TeamUpdate(TeamBase):
    pass


class Team(TeamBase):
    id: int

    class Config:
        orm_mode = True


class SeasonBase(BaseModel):
    year: int
    wikipedia: t.Optional[str] = None


class SeasonCreate(SeasonBase):
    pass


class SeasonUpdate(SeasonBase):
    pass


class Season(SeasonBase):
    id: int

    class Config:
        orm_mode = True


class RoundBase(BaseModel):
    reference: t.Optional[str] = None
    name: str
    round_number: int
    date: t.Optional[date] = None
    time: t.Optional[str] = None
    wikipedia: t.Optional[str] = None
    season_id: int
    circuit_id: int


class RoundCreate(RoundBase):
    pass


class RoundUpdate(RoundBase):
    pass


class Round(RoundBase):
    id: int

    class Config:
        orm_mode = True


class SessionBase(BaseModel):
    session_type: str
    date: t.Optional[date] = None
    time: t.Optional[str] = None
    status: t.Optional[str] = None
    round_id: int


class SessionCreate(SessionBase):
    pass


class SessionUpdate(SessionBase):
    pass


class Session(SessionBase):
    id: int

    class Config:
        orm_mode = True


class TeamDriverBase(BaseModel):
    season_year: int
    team_id: int
    driver_id: int


class TeamDriverCreate(TeamDriverBase):
    pass


class TeamDriverUpdate(TeamDriverBase):
    pass


class TeamDriver(TeamDriverBase):
    id: int

    class Config:
        orm_mode = True


class ResultBase(BaseModel):
    position: t.Optional[int] = None
    position_text: t.Optional[str] = None
    points: t.Optional[float] = None
    grid: t.Optional[int] = None
    laps: t.Optional[int] = None
    status: t.Optional[str] = None
    time_millis: t.Optional[int] = None
    fastest_lap: t.Optional[int] = None
    fastest_lap_time: t.Optional[str] = None
    session_id: int
    driver_id: int
    team_id: int


class ResultCreate(ResultBase):
    pass


class ResultUpdate(ResultBase):
    pass


class Result(ResultBase):
    id: int

    class Config:
        orm_mode = True
