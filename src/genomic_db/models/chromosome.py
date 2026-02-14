"""Chromosome model — a chromosome record, linked to a specific genome."""

from datetime import datetime
from sqlalchemy import ForeignKey, String, DateTime, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from genomic_db.models.base import Base


class Chromosome(Base):
    """A chromosome record, linked to a specific genome."""
    __tablename__ = "chromosomes"
    __table_args__ = (
        UniqueConstraint("name", "genome_id"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))  # e.g., "chr1", "chrX"
    length: Mapped[int | None] = mapped_column(nullable=True)  # base pairs

    # Foreign key to parent genome
    genome_id: Mapped[int] = mapped_column(ForeignKey("genomes.id"))

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    # Relationships
    genome: Mapped["Genome"] = relationship(back_populates="chromosomes")
    genes: Mapped[list["Gene"]] = relationship(
        back_populates="chromosome",
        cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Chromosome(id={self.id}, name='{self.name}', genome_id={self.genome_id})>"


# Resolve forward references
from genomic_db.models.genome import Genome  # noqa: E402, F401
from genomic_db.models.gene import Gene  # noqa: E402, F401
