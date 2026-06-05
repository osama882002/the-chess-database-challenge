"""
=========================================================
QUERIES MODULE
=========================================================

Purpose:
--------
Execute SQL queries and return results.

Contains:

1. query()
2. run_assignment()
3. explain_query_plan()
4. run_assignment_extended()

=========================================================
"""

import sqlite3
from src.logger import logger
import pandas as pd



def query(conn: sqlite3.Connection, sql: str) -> pd.DataFrame:
    """
    Execute SQL query and return DataFrame.

    Parameters
    ----------
    conn:
        SQLite connection

    sql:
        SQL statement

    Returns
    -------
    pandas DataFrame
    """

    return pd.read_sql(sql, conn)

def run_assignment(conn: sqlite3.Connection) -> None:

    # ==================================================
    # STAGE 1
    # ==================================================

    print("\n" + "=" * 60)
    print("STAGE 1 - SELECT")
    logger.info("=" * 60)
    logger.info("Start STAGE 1")
    print("=" * 60)

    # ==================================================
    # Q1
    # How many games exist?
    # How many are rated?
    # ==================================================

    q1 = query(
        conn,
        """
        SELECT

            COUNT(*) AS total_games,

            SUM(rated) AS rated_games

        FROM games
        """
    )

    print("\nQ1")
    print(q1)
    logger.info("Q1: Total games and rated games. Done ✅")

    # ==================================================
    # Q2
    # List all distinct victory_status values and their counts
    # ==================================================

    q2 = query(
        conn,
        """
        SELECT

            victory_status,

            COUNT(*) AS total

        FROM games

        GROUP BY victory_status

        ORDER BY total DESC
        """
    )

    print("\nQ2 List all distinct victory_status values and their counts")
    print(q2)
    logger.info("Q2: List all distinct victory_status values and their counts. Done ✅")

    # ==================================================
    # Q3
    # What are the 10 games with the most turns? 
    # Show game_id, winner, turns.
    # ==================================================

    q3 = query(
        conn,
        """
        SELECT

            game_id,
            winner,
            turns

        FROM games

        ORDER BY turns DESC

        LIMIT 10
        """
    )

    print("\nQ3 Top 10 Longest Games")
    print(q3)
    logger.info("Q3: Top 10 Longest Games. Done ✅")

    # ==================================================
    # Q4 
    # What is the win rate (%) for White, Black, and Draw across all games?
    # ==================================================

    q4 = query(
        conn,
        """
        SELECT

            winner,

            ROUND(
                COUNT(*) * 100.0
                /
                (
                    SELECT COUNT(*)
                    FROM games
                ),
                2
            ) AS win_rate

        FROM games

        GROUP BY winner
        """
    )

    print("\nQ4 Win Rate")
    print(q4)
    logger.info("Q4: Win Rate. Done ✅")
    logger.info("STAGE 1 Done ✅")

    # ==================================================
    # STAGE 2
    # ==================================================

    print("\n" + "=" * 60)
    print("STAGE 2 - GROUP BY")
    logger.info("=" * 60)
    logger.info("Start STAGE 2")
    print("=" * 60)

    # ==================================================
    # Q5 
    # For each victory_status, what is the average and max number of turns? 
    # Sort highest avg first.
    # ==================================================

    q5 = query(
        conn,
        """
        SELECT

            victory_status,

            ROUND(
                AVG(turns),
                2
            ) AS avg_turns,

            MAX(turns) AS max_turns

        FROM games

        GROUP BY victory_status

        ORDER BY avg_turns DESC
        """
    )

    print("\nQ5 Average + Max Turns")
    print(q5)
    logger.info("Q5 Average + Max Turns. Done ✅")

    # ==================================================
    # Q6 
    # Which 5 opening_codes appear most frequently? 
    # Use HAVING to show only those with more than 500 games.
    # ==================================================

    q6 = query(
        conn,
        """
        SELECT

            opening_code,

            COUNT(*) AS total_games

        FROM games

        GROUP BY opening_code

        HAVING COUNT(*) > 500

        ORDER BY total_games DESC
        """
    )

    print("\nQ6 The 5 opening_codes appear most frequently")
    print(q6)
    logger.info("Q6 The 5 opening_codes appear most frequently. Done ✅")

    logger.info("STAGE 2 Done ✅")