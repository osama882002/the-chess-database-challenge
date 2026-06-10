"""
=========================================================
BUILDER MODULE
=========================================================

Purpose:
--------
Load data into the database.

Responsibilities:

1. Build Players table
2. Build Openings table
3. Build Games table
4. Create Indexes

This file is responsible for:

DataFrame → SQLite

Nothing else.

=========================================================
"""

import sqlite3
import pandas as pd
from src.logger import logger


def build_tables(conn: sqlite3.Connection, chess: pd.DataFrame) -> None:
    """
    Load all data into database tables.

    Insertion Order:

        players
            ↓

        openings
            ↓

        games

    Why?

    Because games contains foreign keys
    that reference players and openings.

    Therefore parent tables must exist first.
    """

    # =====================================================
    # PLAYERS TABLE
    # =====================================================

    """
    Build player dimension table.

    We collect:

        white players
        black players

    Then combine them.

    Goal:

        One row per player.
    """

    white = (
        chess[
            ["white_id", "white_rating"]
        ]
        .rename(
            columns={
                "white_id": "username",
                "white_rating": "rating"
            }
        )
    )

    black = (
        chess[
            ["black_id", "black_rating"]
        ]
        .rename(
            columns={
                "black_id": "username",
                "black_rating": "rating"
            }
        )
    )

    # Combine both sides

    players_df = (
        pd.concat(
            [white, black]
        )
        .groupby("username")["rating"]
        .last()
        .reset_index()
        .rename(
            columns={
                "rating": "last_rating"
            }
        )
    )

    """
    Count total appearances.

    Example:

        Magnus appears:

            10 times as White
            15 times as Black

        total_games = 25
    """

    white_counts = (
        chess["white_id"]
        .value_counts()
        .rename("white_games")
    )

    black_counts = (
        chess["black_id"]
        .value_counts()
        .rename("black_games")
    )

    players_df["total_games"] = (
        players_df["username"]
        .map(
            white_counts.add(
                black_counts,
                fill_value=0
            )
        )
        .astype(int)
    )

    players_df.to_sql(
        "players",
        conn,
        if_exists="append",
        index=False
    )

    logger.info(
        f"Players loaded: {len(players_df):,}"
    )

    # =====================================================
    # OPENINGS TABLE
    # =====================================================

    """
    Opening dimension table.

    One row per opening code.
    """

    openings_df = (
        chess[
            [
                "opening_code",
                "opening_shortname",
                "opening_fullname"
            ]
        ]
        .drop_duplicates(
            subset="opening_code"
        )
        .reset_index(drop=True)
    )

    openings_df.to_sql(
        "openings",
        conn,
        if_exists="append",
        index=False
    )

    logger.info(
        f"Openings loaded: {len(openings_df):,}"
    )

    # =====================================================
    # GAMES TABLE
    # =====================================================

    """
    Fact table.

    One row per chess game.
    """

    games_df = chess[
        [
            "game_id",
            "white_id",
            "black_id",
            "winner",
            "victory_status",
            "turns",
            "time_increment",
            "rated",
            "opening_code",
            "white_rating",
            "black_rating"
        ]
    ].copy()

    games_df.to_sql(
        "games",
        conn,
        if_exists="append",
        index=False
    )

    logger.info(
        f"Games loaded: {len(games_df):,}"
    )

    logger.info(
        "All tables loaded successfully."
    )


def create_indexes(conn: sqlite3.Connection) -> None:
    """
    Create indexes.

    Indexes speed up:

        WHERE
        JOIN
        ORDER BY

    operations.

    Especially important for large datasets.
    """

    # =====================================================
    # PLAYER LOOKUPS
    # =====================================================

    conn.execute(
        """
        CREATE INDEX IF NOT EXISTS
        idx_games_white
        ON games(white_id)
        """
    )

    conn.execute(
        """
        CREATE INDEX IF NOT EXISTS
        idx_games_black
        ON games(black_id)
        """
    )

    # =====================================================
    # OPENING LOOKUPS
    # =====================================================

    conn.execute(
        """
        CREATE INDEX IF NOT EXISTS
        idx_games_opening
        ON games(opening_code)
        """
    )

    # =====================================================
    # WINNER LOOKUPS
    # =====================================================

    conn.execute(
        """
        CREATE INDEX IF NOT EXISTS
        idx_games_winner
        ON games(winner)
        """
    )

    logger.info(
        "Indexes created successfully."
    )
