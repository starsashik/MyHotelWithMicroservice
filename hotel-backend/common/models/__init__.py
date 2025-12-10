"""Общие модели данных для всех микросервисов."""

from common.models.base import Base
from common.models.user import User
from common.models.hotel import Hotel
from common.models.room import Room
from common.models.booking import Booking
from common.models.log import LogEntry

__all__ = [
    "Base",
    "User",
    "Hotel",
    "Room",
    "Booking",
    "LogEntry",
]

