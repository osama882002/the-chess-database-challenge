"""
=========================================================
SCHEMA MODULE
=========================================================

Purpose:
--------
Create the database schema from scratch.

This file is responsible ONLY for:

1. Creating tables
2. Defining relationships
3. Defining constraints
4. Enforcing data integrity

No data loading happens here.
No SQL analysis queries happen here.

Think of this file as:
"The blueprint of the database"
=========================================================
"""

import sqlite3
from src.logger import logger


# Logger used for tracking execution



def create_schema(conn: sqlite3.Connection) -> None:
    """
    Create all database tables.

    Tables:
    -------
    players
    openings
    games

    Relationships:
    --------------
    games.white_id  -> players.username
    games.black_id  -> players.username
    games.opening_code -> openings.opening_code

    Why create tables manually?

    Because pandas.to_sql():

        - doesn't create foreign keys
        - doesn't create check constraints
        - doesn't create proper PKs

    In production databases we always
    define the schema explicitly.
    """

    # =====================================================
    # DROP TABLES
    # =====================================================

    """
    Drop tables before recreation.

    Order matters.

    games depends on:
        players
        openings

    Therefore:

        games
        openings
        players

    Reverse dependency order.
    """

    conn.execute(
        "DROP TABLE IF EXISTS games"
    )

    conn.execute(
        "DROP TABLE IF EXISTS openings"
    )

    conn.execute(
        "DROP TABLE IF EXISTS players"
    )

    logger.info("Old tables removed.")

    # =====================================================
    # PLAYERS TABLE
    # =====================================================

    """
    One row per player.

    username:
        unique identifier

    last_rating:
        latest rating observed

    total_games:
        total games played
    """

    conn.execute(
        """
        CREATE TABLE players (

            username TEXT
                PRIMARY KEY
                NOT NULL,

            last_rating INTEGER
                NOT NULL,

            total_games INTEGER
                NOT NULL
                DEFAULT 0
        )
        """
    )

    logger.info("Players table created.")

    # =====================================================
    # OPENINGS TABLE
    # =====================================================

    """
    One row per opening code.

    Example:

        B01
        Sicilian Defense
        Sicilian Defense: Scandinavian Variation
    """

    conn.execute(
        """
        CREATE TABLE openings (

            opening_code TEXT
                PRIMARY KEY
                NOT NULL,

            opening_shortname TEXT
                NOT NULL,

            opening_fullname TEXT
                NOT NULL
        )
        """
    )

    logger.info("Openings table created.")

    # =====================================================
    # GAMES TABLE
    # =====================================================

    """
    Central fact table.

    Every chess game is stored here.

    Foreign Keys:

        white_id
        black_id

    reference players table.

        opening_code

    references openings table.
    """

    conn.execute(
        """
        CREATE TABLE games (

            game_id INTEGER
                PRIMARY KEY
                NOT NULL,

            white_id TEXT
                NOT NULL
                REFERENCES players(username),

            black_id TEXT
                NOT NULL
                REFERENCES players(username),

            winner TEXT
                NOT NULL
                CHECK(
                    winner IN (
                        'White',
                        'Black',
                        'Draw'
                    )
                ),

            victory_status TEXT
                NOT NULL,

            turns INTEGER
                NOT NULL
                CHECK(turns >= 1),

            time_increment TEXT
                NOT NULL,

            rated INTEGER
                NOT NULL
                CHECK(
                    rated IN (0,1)
                ),

            opening_code TEXT
                NOT NULL
                REFERENCES openings(
                    opening_code
                ),

            white_rating INTEGER
                NOT NULL,

            black_rating INTEGER
                NOT NULL
        )
        """
    )

    logger.info("Games table created.")

    # =====================================================
    # FINISHED
    # =====================================================

    logger.info("Schema created successfully.")

