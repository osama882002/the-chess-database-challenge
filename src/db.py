"""
=========================================================
MAIN PIPELINE
=========================================================

Execution Flow:

Create Schema
    ↓

Build Tables
    ↓

Create Indexes
    ↓

Validate
    ↓

Run Assignment
    ↓

Run Extended Assignment
    ↓

Export Outputs

=========================================================
"""

import os
import sqlite3
import pandas as pd

from src.logger import logger
from src.schema import create_schema
from src.builder import (
    build_tables,
    create_indexes
)
from src.validator import (
    verify_schema, 
    verify_indexes
)
from src.queries import (
    run_assignment,
    explain_query_plan,
    run_assignment_extended,
)
from src.exporter import (
    export_features,
    export_game_ranks
)




def main():

    logger.info("=== CHESS DATABASE PIPELINE ===")
    print("\n=== CHESS DATABASE PIPELINE ===\n")

    # ==================================================
    # LOAD CSV
    # ==================================================

    chess = pd.read_csv(
        os.path.join(
            "data",
            "raw",
            "chess_games.csv"
        )
    )

    print(
        f"Loaded dataset: "
        f"{len(chess):,} rows"
    )
    logger.info(
        f"Loaded dataset: "
        f"{len(chess):,} rows"
    )

    # ==================================================
    # CONNECT DATABASE
    # ==================================================

    db_path = os.path.join(
        "data",
        "processed",
        "chess.db"
    )

    conn = sqlite3.connect(db_path)

    conn.execute("PRAGMA foreign_keys = ON")

    # ==================================================
    # SCHEMA
    # ==================================================

    create_schema(conn)

    # ==================================================
    # LOAD TABLES
    # ==================================================

    build_tables(conn, chess)

    create_indexes(conn)

    # ==================================================
    # VALIDATION
    # ==================================================

    verify_schema(conn)
    verify_indexes(conn)

    # ==================================================
    # ASSIGNMENT
    # ==================================================

    run_assignment(conn)

    # ==================================================
    # EXTENDED
    # ==================================================

    explain_query_plan(conn)

    # ==================================================
    # ASSIGNMENT EXTENDED
    # ==================================================


    run_assignment_extended(conn)
    
    # ==================================================
    # EXPORTS
    # ==================================================

    export_features(conn)

    export_game_ranks(conn)

    conn.commit()

    conn.close()

    print("\nDatabase pipeline completed.")
    logger.info("Database pipeline completed. Done ✅")

if __name__ == "__main__":
    main()