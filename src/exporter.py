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

        game_id,

        white_rating - black_rating
            AS rating_diff,

        turns,

        rated,

        opening_shortname,

        winner

    FROM games g

    JOIN openings o

        ON g.opening_code = o.opening_code
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
    """

    ranks_df = pd.read_sql(sql, conn)

    output_path = os.path.join(OUTPUT_DIR, "game_ranks.csv")

    ranks_df.to_csv(output_path, index=False)

    logger.info(f"Game ranks exported: {output_path}")
    print(f"Game ranks exported: {output_path}")
