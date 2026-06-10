"""
=========================================================
EXPORTER MODULE
=========================================================

Purpose:
--------
Export analytical outputs from SQLite
into CSV files.

Responsibilities:

1. Feature Table Export
2. Ranked Games Export

=========================================================
"""

import os
import sqlite3
import pandas as pd
from src.logger import logger



OUTPUT_DIR = os.path.join("data", "processed")

os.makedirs(OUTPUT_DIR, exist_ok=True)


def export_features(conn: sqlite3.Connection) -> None:
    """
    Build feature table.

    Output:

    features.csv
    """

    sql = """
    SELECT

        g.game_id,

        g.white_rating - g.black_rating
            AS rating_diff,

        g.turns,

        g.rated,

        o.opening_shortname,

        COALESCE(
            p.total_games, 0
        ) AS white_experience,

        g.winner AS label

    FROM games g

    JOIN openings o

        ON g.opening_code = o.opening_code

    LEFT JOIN players p
        ON g.white_id = p.username    
    """

    features_df = pd.read_sql(sql, conn)

    output_path = os.path.join(OUTPUT_DIR, "features.csv")

    features_df.to_csv(output_path, index=False)

    logger.info(f"Feature table exported: {output_path}")
    print(f"Feature table exported: {output_path}")


def export_game_ranks(conn: sqlite3.Connection) -> None:
    """
    Assignment Extended

    Rank games by turns.

    Longest game = Rank 1
    """

    sql = """
    SELECT

        game_id,

        white_id,

        turns,

        RANK() OVER (

            PARTITION BY white_id

            ORDER BY turns DESC

        ) AS turns_rank

    FROM games
    ORDER BY
        white_id,
        turns_rank
    """

    ranks_df = pd.read_sql(sql, conn)

    output_path = os.path.join(OUTPUT_DIR, "game_ranks.csv")

    ranks_df.to_csv(output_path, index=False)

    logger.info(f"Game ranks exported: {output_path}")
    print(f"Game ranks exported: {output_path}")

