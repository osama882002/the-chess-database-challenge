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

    # ==================================================
    # STAGE 3
    # ==================================================
    print("\n" + "=" * 60)
    print("STAGE 3 - JOINS & CTEs")
    logger.info("=" * 60)
    logger.info("Start STAGE 3")
    print("=" * 60)

    # ==================================================
    # Q7 
    # JOIN games to openings
    # find the 5 most played openings with their full name.
    # ==================================================

    q7 = query(
        conn,
        """
        SELECT

            o.opening_code,

            o.opening_fullname,

            COUNT(*) AS total_games

        FROM games g

        JOIN openings o

            ON g.opening_code = o.opening_code

        GROUP BY

            o.opening_code,
            o.opening_fullname

        ORDER BY total_games DESC

        LIMIT 5
        """
    )

    print("\nQ7 - Most Played Openings")

    print(q7)
    logger.info("Q7 Find the 5 most played openings with their full name. Done ✅")

    # ==================================================
    # Q8 
    # LEFT JOIN players to games: 
    # find any players in the players table who have never appeared as white_id.
    # ==================================================

    q8 = query(
        conn,
        """
        SELECT

            p.username

        FROM players p

        LEFT JOIN games g

            ON p.username = g.white_id

        WHERE g.white_id IS NULL
        """
    )

    print("\nQ8 - Players Never Appearing As White")

    print(q8.head())
    logger.info("Q8 Players Never Appearing As White. Done ✅")


    # ==================================================
    # Q9 
    # Using a CTE: compute total wins per player (as white). 
    # Return top 5.
    # ==================================================

    q9 = query(
        conn,
        """
        WITH white_wins AS (

            SELECT

                white_id,

                COUNT(*) AS wins

            FROM games

            WHERE winner = 'White'

            GROUP BY white_id
        )

        SELECT *

        FROM white_wins

        ORDER BY wins DESC

        LIMIT 5
        """
    )

    print("\nQ9 - Top 5 White Winners")

    print(q9)
    logger.info("Q9 Return Top 5 White Winners. Done ✅")

    # ==================================================
    # Q10 
    # UNION CTE: combine white wins and black wins into one 'player_wins' table. 
    # Who has the most total wins?
    # ==================================================

    q10 = query(
        conn,
        """
        WITH player_wins AS (

            SELECT

                white_id AS player,

                COUNT(*) AS wins

            FROM games

            WHERE winner = 'White'

            GROUP BY white_id

            UNION ALL

            SELECT

                black_id AS player,

                COUNT(*) AS wins

            FROM games

            WHERE winner = 'Black'

            GROUP BY black_id
        )

        SELECT

            player,

            SUM(wins) AS total_wins

        FROM player_wins

        GROUP BY player

        ORDER BY total_wins DESC

        LIMIT 1
        """
    )

    print("\nQ10 - Player With Most Total Wins")
    print(q10)
    logger.info("Q10 Player With Most Total Wins. Done ✅")

    logger.info("STAGE 3 Done ✅")


    # ==================================================
    # STAGE 4
    # ==================================================


    print("\n" + "=" * 60)
    print("STAGE 4 - WINDOW FUNCTIONS")
    logger.info("=" * 60)
    logger.info("Start STAGE 4")
    print("=" * 60)

    # ==================================================
    # Q11 
    # Window function: for each game, add a column showing what RANK each game holds for that white player by white_rating (highest rating = rank 1). 
    # Show top 10 rows.
    # ==================================================

    q11 = query(
        conn,
        """
        SELECT

            game_id,

            white_id,

            white_rating,

            RANK() OVER (

                PARTITION BY white_id

                ORDER BY white_rating DESC

            ) AS rating_rank

        FROM games

        LIMIT 10
        """
    )

    print("\nQ11 - Top 10 Rating Rank")
    print(q11)

    logger.info("Q11 Top 10 Rating Rank. Done ✅")

    # ==================================================
    # Q12 
    # LAG: show each game's white_rating and the previous game's white_rating for the same player. 
    # Filter to players with 5+ games.
    # ==================================================

    q12 = query(
        conn,
        """
        WITH player_games AS (

            SELECT

                game_id,

                white_id,

                white_rating,

                LAG(
                    white_rating
                ) OVER (

                    PARTITION BY white_id

                    ORDER BY game_id

                ) AS previous_rating

            FROM games
        )

        SELECT *

        FROM player_games

        WHERE white_id IN (

            SELECT white_id

            FROM games

            GROUP BY white_id

            HAVING COUNT(*) >= 5
        )

        LIMIT 10
        """
    )

    print("\nQ12 - Previous Rating")
    print(q12)

    logger.info("Q12 Compare current rating with previous game. Done ✅")

    logger.info("STAGE 4 Done ✅")




def explain_query_plan(conn, sql):
    """
    Show SQLite execution plan.
    """

    result = conn.execute(f"EXPLAIN QUERY PLAN {sql}").fetchall()

    print("\nQuery Plan:")

    for row in result:
        print(row)

    logger.info("EXPLAIN QUERY PLAN executed Done ✅")