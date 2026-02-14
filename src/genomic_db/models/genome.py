"""Genome model — a genome record in the dataset."""

from datetime import datetime
from sqlalchemy import String, Text, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from genomic_db.models.base import Base


class Genome(Base):
    """A genome record in the dataset (e.g., GRCh38, GRCm39)."""
    __tablename__ = "genomes"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), unique=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Timestamps for tracking
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    # Relationship: one genome has many chromosomes
    chromosomes: Mapped[list["Chromosome"]] = relationship(
        back_populates="genome",
        cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Genome(id={self.id}, name='{self.name}')>"


# Resolve forward reference
from genomic_db.models.chromosome import Chromosome  # noqa: E402, F401
