#!/usr/bin/env python3
"""Example script demonstrating basic database operations.

This creates sample data to verify the schema works correctly.

Usage:
    # Start Postgres first
    docker compose up -d
    
    # Run migrations
    alembic upgrade head
    
    # Run this script
    python scripts/example_usage.py
"""

from genomic_db.db import get_session, engine
from genomic_db.models import Base, Genome, Chromosome, Gene


def create_sample_data():
    """Create sample genomic data."""
    
    # Create tables (in production, use Alembic migrations instead)
    Base.metadata.create_all(engine)
    
    session = get_session()
    
    try:
        # Check if we already have data
        existing = session.query(Genome).filter_by(name="Example Genome").first()
        if existing:
            print(f"Sample data already exists: {existing}")
            return
        
        # Create a genome
        genome = Genome(
            name="Example Genome",
            description="A minimal example genome for testing"
        )
        session.add(genome)
        session.flush()  # Get the genome.id
        
        # Create chromosomes
        chr1 = Chromosome(name="chr1", length=1000000, genome_id=genome.id)
        chr2 = Chromosome(name="chr2", length=800000, genome_id=genome.id)
        session.add_all([chr1, chr2])
        session.flush()
        
        # Create genes on chromosome 1
        gene_a = Gene(
            name="GENE_A",
            start_position=1000,
            end_position=2500,
            strand="+",
            sequence="ATGCGTACGATCGATCGATCG",
            chromosome_id=chr1.id
        )
        gene_b = Gene(
            name="GENE_B",
            start_position=5000,
            end_position=7000,
            strand="-",
            sequence="GCTAGCTAGCTAGCTAGCTA",
            chromosome_id=chr1.id
        )
        
        # Create a gene on chromosome 2
        gene_c = Gene(
            name="GENE_C",
            start_position=100,
            end_position=500,
            strand="+",
            sequence="TTAACCGGTTAACCGGTTAA",
            chromosome_id=chr2.id
        )
        
        session.add_all([gene_a, gene_b, gene_c])
        session.commit()
        
        print("Created sample data:")
        print(f"  Genome: {genome}")
        print(f"  Chromosomes: {chr1}, {chr2}")
        print(f"  Genes: {gene_a}, {gene_b}, {gene_c}")
        
    finally:
        session.close()


def query_examples():
    """Demonstrate querying the hierarchical data."""
    
    session = get_session()
    
    try:
        # Get a genome and traverse down
        genome = session.query(Genome).filter_by(name="Example Genome").first()
        
        if not genome:
            print("No sample data found. Run create_sample_data() first.")
            return
        
        print(f"\n--- Querying {genome.name} ---")
        
        # Access chromosomes through relationship
        print(f"\nChromosomes ({len(genome.chromosomes)}):")
        for chrom in genome.chromosomes:
            print(f"  {chrom.name}: {len(chrom.genes)} genes")
            
            # Access genes through relationship
            for gene in chrom.genes:
                print(f"    - {gene.name} ({gene.strand}) at {gene.start_position}-{gene.end_position}")
        
        # Direct gene query with join
        print("\n--- All genes with their chromosome and genome ---")
        genes = (
            session.query(Gene)
            .join(Chromosome)
            .join(Genome)
            .filter(Genome.name == "Example Genome")
            .all()
        )
        for gene in genes:
            # Navigate up the hierarchy
            print(f"{gene.name} -> {gene.chromosome.name} -> {gene.chromosome.genome.name}")
        
    finally:
        session.close()


if __name__ == "__main__":
    print("=== Creating Sample Data ===")
    create_sample_data()
    
    print("\n=== Query Examples ===")
    query_examples()
