import sqlite3
import pandas as pd
from src.logger import logger

def create_schema(conn: sqlite3.Connection) -> None:
    """
    We need to create and normalize 3 tables out of the csv data:
    Players, Openings, Games
    
    Define all three tables with explicit types, PRIMARY KEYs,
    FOREIGN KEYs, NOT NULL constraints, and CHECK constraints.

    Why explicit CREATE TABLE instead of letting to_sql() infer?
    - to_sql() creates columns with no constraints whatsoever
    - FK relationships would exist in comments only, not enforced
    - CHECK constraints (winner IN (...), turns >= 1) would be absent
    - NOT NULL would not be set on any column
    - Column types would be SQLite affinity guesses, not intentional choices

    Insertion order matters:
      players and openings must exist before games,
      because games has FK references to both.
    """

    # Drop in reverse FK dependency order so re-runs are clean
    conn.execute("DROP TABLE IF EXISTS games")
    conn.execute("DROP TABLE IF EXISTS openings")
    conn.execute("DROP TABLE IF EXISTS players")


    # Players: one raw per uniqu player. 
    conn.execute("""
        CREATE TABLE players (
            username     TEXT    PRIMARY KEY NOT NULL,
            last_rating  INTEGER NOT NULL,
            total_games  INTEGER NOT NULL DEFAULT 0
        )
    """)

    # Openings: one row per unique opening code.
    conn.execute("""
        CREATE TABLE openings (
            opening_code      TEXT PRIMARY KEY NOT NULL,
            opening_shortname TEXT NOT NULL,
            opening_fullname  TEXT NOT NULL
        )
    """)

    # Games: The core table 
    # White_id and Black_id are foreign keys to players.username
    # Opening_code is a foreign key to openings.opening_code
    # I'm gonna keep the ratings even though in normalzation we can driv them from players. 
    # This is a delibrate de-normalization for analytical convenience.
    conn.execute("""
        CREATE TABLE games (
            game_id        INTEGER PRIMARY KEY NOT NULL,
            white_id       TEXT    NOT NULL
                                REFERENCES players(username),
            black_id       TEXT    NOT NULL
                                REFERENCES players(username),
            winner         TEXT    NOT NULL
                                CHECK(winner IN ('White', 'Black', 'Draw')),
            victory_status TEXT    NOT NULL,
            turns          INTEGER NOT NULL
                                CHECK(turns >= 1),
            time_increment TEXT    NOT NULL,
            rated          INTEGER NOT NULL
                                CHECK(rated IN (0, 1)),
            opening_code   TEXT    NOT NULL
                                REFERENCES openings(opening_code),
            white_rating   INTEGER NOT NULL,
            black_rating   INTEGER NOT NULL
        )
    """)
    
    
    logger.info("Schema created: players, openings, games (with FK + CHECK constraints)")


def verify_schema(conn: sqlite3.Connection) -> None:
    """
    Assert expected row counts AND confirm FK/CHECK constraints are present.
    Reads the CREATE TABLE SQL from sqlite_master and checks for key phrases.
    """
    # Row counts
    for table, expected in [("players", 15635), ("openings", 365), ("games", 20058)]:
        actual = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        assert actual == expected, f"Expected {expected} rows in {table}, but got {actual}."
        logger.info(f"✅ Verified {table} table: {actual} rows.")

    # Constraint verification — read the stored DDL from sqlite_master
    ddl_rows = conn.execute(
        "SELECT name, sql FROM sqlite_master WHERE type='table' ORDER BY name"
    ).fetchall()
    ddl = {name: sql for name, sql in ddl_rows}

    # players: must have PRIMARY KEY
    assert "PRIMARY KEY" in ddl["players"], "players: missing PRIMARY KEY"

    # openings: must have PRIMARY KEY
    assert "PRIMARY KEY" in ddl["openings"], "openings: missing PRIMARY KEY"

    # games: must have FKs and CHECK constraints
    assert "REFERENCES players" in ddl["games"],  "games: missing FK to players"
    assert "REFERENCES openings" in ddl["games"], "games: missing FK to openings"
    assert "CHECK" in ddl["games"],               "games: missing CHECK constraints"
    assert "winner IN" in ddl["games"],            "games: missing winner CHECK"
    assert "turns >= 1" in ddl["games"],           "games: missing turns CHECK"

    logger.info("✓ Schema constraints verified: PKs, FKs, CHECK all present")

    # Verify FK enforcement is active
    fk_status = conn.execute("PRAGMA foreign_keys").fetchone()[0]
    assert fk_status == 1, "PRAGMA foreign_keys is OFF — FKs will not be enforced"
    logger.info("✓ PRAGMA foreign_keys = ON confirmed")
