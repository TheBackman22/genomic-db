"""Gene model — a gene record, linked to a specific chromosome."""

from datetime import datetime
from sqlalchemy import ForeignKey, String, Text, DateTime, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from genomic_db.models.base import Base


class Gene(Base):
    """A gene record, linked to a specific chromosome."""
    __tablename__ = "genes"
    __table_args__ = (
        UniqueConstraint("name", "chromosome_id"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))

    # Position on chromosome
    start_position: Mapped[int] = mapped_column()
    end_position: Mapped[int] = mapped_column()
    strand: Mapped[str | None] = mapped_column(String(1), nullable=True)  # '+' or '-'

    # The actual sequence (base pairs as text)
    sequence: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Foreign key to parent chromosome
    chromosome_id: Mapped[int] = mapped_column(ForeignKey("chromosomes.id"))

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    # Relationship
    chromosome: Mapped["Chromosome"] = relationship(back_populates="genes")

    @property
    def length(self) -> int:
        """Calculate gene length from positions."""
        return self.end_position - self.start_position

    def __repr__(self) -> str:
        return f"<Gene(id={self.id}, name='{self.name}', pos={self.start_position}-{self.end_position})>"


# Resolve forward reference
from genomic_db.models.chromosome import Chromosome  # noqa: E402, F401
