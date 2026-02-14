import pytest
from genomic_db.models import Genome, Chromosome, Gene

class ModelTests:
    """Basic tests for genomic models"""
    """Run with pytest using `pytest tests/test_models.py`"""

    def test_genome_creation(self):
        """Test that Genome model can be instantiated."""
        genome = Genome(name="Test Genome", description="A test")
        assert genome.name == "Test Genome"
        assert genome.description == "A test"


    def test_chromosome_creation(self):
        """Test that Chromosome model can be instantiated."""
        chrom = Chromosome(name="chr1", length=100000, genome_id=1)
        assert chrom.name == "chr1"
        assert chrom.length == 100000


    def test_gene_creation(self):
        """Test that Gene model can be instantiated."""
        gene = Gene(
            name="BRCA1",
            start_position=1000,
            end_position=5000,
            strand="+",
            sequence="ATGC",
            chromosome_id=1
        )
        assert gene.name == "BRCA1"
        assert gene.length == 4000  # 5000 - 1000


    def test_gene_length_property(self):
        """Test the computed length property."""
        gene = Gene(
            name="TEST",
            start_position=100,
            end_position=350,
            chromosome_id=1
        )
        assert gene.length == 250
