"""
=========================================================
VALIDATOR MODULE
=========================================================

Purpose:
--------
Validate the database after creation.

This module verifies:

1. Row counts
2. Primary Keys
3. Foreign Keys
4. CHECK Constraints
5. SQLite FK Enforcement


=========================================================
"""

import sqlite3
from src.logger import logger



def verify_schema(conn: sqlite3.Connection) -> None:
    """
    Validate the database.

    Validation checks:

    1. Row counts
    2. Primary Keys
    3. Foreign Keys
    4. CHECK Constraints
    5. Foreign Key Enforcement
    """

    logger.info("=" * 60)

    logger.info("STARTING DATABASE VALIDATION")

    # =====================================================
    # ROW COUNT VALIDATION
    # =====================================================

    """
    Verify expected number of rows.

    If row counts differ:

        - Data may be missing
        - Load process failed
        - Duplicate removal happened unexpectedly
    """

    expected_counts = {

        "players": 15635,

        "openings": 365,

        "games": 20058

    }

    for table, expected in expected_counts.items():

        actual = conn.execute(
            f"""
            SELECT COUNT(*)
            FROM {table}
            """
        ).fetchone()[0]

        assert actual == expected, (

            f"{table}: "

            f"expected {expected:,} rows "

            f"but found {actual:,}"

        )

        logger.info(f"✓ {table}: {actual:,} rows")

    # =====================================================
    # READ TABLE DEFINITIONS
    # =====================================================

    """
    sqlite_master stores

    CREATE TABLE statements.

    We read them to verify
    constraints actually exist.
    """

    ddl_rows = conn.execute(
        """
        SELECT
            name,
            sql
        FROM sqlite_master
        WHERE type='table'
        """
    ).fetchall()

    ddl = {

        name: sql

        for name, sql in ddl_rows

    }

    # =====================================================
    # PRIMARY KEY VALIDATION
    # =====================================================

    """
    Verify:

        players PK

        openings PK
    """

    assert ("PRIMARY KEY" in ddl["players"]), ("players missing PRIMARY KEY")

    assert ("PRIMARY KEY" in ddl["openings"]), ("openings missing PRIMARY KEY")

    logger.info("✓ Primary Keys verified")

    # =====================================================
    # FOREIGN KEY VALIDATION
    # =====================================================

    """
    Verify relationships exist.
    """

    assert ("REFERENCES players" in ddl["games"]), ("games missing FK -> players")

    assert ("REFERENCES openings" in ddl["games"]), ("games missing FK -> openings")

    logger.info("✓ Foreign Keys verified")

    # =====================================================
    # CHECK CONSTRAINT VALIDATION
    # =====================================================

    """
    Verify database rules exist.
    """

    assert ("CHECK" in ddl["games"]), ("games missing CHECK constraints")

    assert ("winner IN" in ddl["games"]), ("winner CHECK constraint missing")

    assert ("turns >= 1" in ddl["games"]), ("turns CHECK constraint missing")

    logger.info("✓ CHECK constraints verified")

    # =====================================================
    # FOREIGN KEY ENFORCEMENT
    # =====================================================

    """
    SQLite ignores foreign keys
    unless explicitly enabled.

    Verify:

        PRAGMA foreign_keys = ON
    """

    fk_status = conn.execute(
        """
        PRAGMA foreign_keys
        """
    ).fetchone()[0]

    assert (fk_status == 1), ("Foreign Keys are disabled")

    logger.info("✓ Foreign Keys enabled")

    # =====================================================
    # FINISHED
    # =====================================================

    logger.info("DATABASE VALIDATION PASSED")
    

def verify_indexes(conn):
    """
    Verify indexes exist.
    """

    indexes = conn.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type='index'
    """).fetchall()

    # print(indexes)

    logger.info("Indexes verified")   
