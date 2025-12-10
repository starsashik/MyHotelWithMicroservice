"""Модель комнаты."""

from decimal import Decimal
from uuid import UUID, uuid4

from sqlalchemy import ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from common.models.base import Base


class Room(Base):
    """Модель комнаты."""

    __tablename__ = "rooms"

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        default=uuid4,
        server_default=None,
    )
    hotel_id: Mapped[UUID] = mapped_column(
        ForeignKey("hotels.id", ondelete="CASCADE"),
        nullable=False,
    )
    room_number: Mapped[str] = mapped_column(String(50), nullable=False)
    room_type: Mapped[int] = mapped_column(nullable=False)
    price_per_night: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )
    img_url: Mapped[str | None] = mapped_column(String(500), nullable=True)

    # Связь с отелем
    hotel: Mapped["Hotel"] = relationship(
        "Hotel",
        back_populates="rooms",
    )

    # Связь с бронированиями
    bookings: Mapped[list["Booking"]] = relationship(
        "Booking",
        back_populates="room",
        cascade="all, delete-orphan",
    )

