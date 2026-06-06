# Database Schema Documentation

## Overview

This project uses a normalized SQLite database called **chess.db** to store and analyze chess game data. The database is organized into three related tables:

1. **players**
2. **openings**
3. **games**

The design follows a relational database approach to reduce redundancy and improve query performance while maintaining data integrity through primary keys, foreign keys, and constraints.

---

# 1. players Table

Stores information about each unique chess player.

| Column      | Data Type | Description                                |
| ----------- | --------- | ------------------------------------------ |
| username    | TEXT      | Unique player identifier                   |
| last_rating | INTEGER   | Most recent rating observed for the player |
| total_games | INTEGER   | Total number of games played by the player |

### Primary Key

* username

### Purpose

The players table prevents player information from being duplicated across thousands of game records and serves as a central reference for player-related queries.

---

# 2. openings Table

Stores unique chess openings.

| Column            | Data Type | Description              |
| ----------------- | --------- | ------------------------ |
| opening_code      | TEXT      | ECO opening code         |
| opening_shortname | TEXT      | Short opening name       |
| opening_fullname  | TEXT      | Full opening description |

### Primary Key

* opening_code

### Purpose

Chess openings repeat across many games. Storing them separately avoids redundant text storage and improves consistency.

---

# 3. games Table

Stores individual chess matches.

| Column         | Data Type | Description                      |
| -------------- | --------- | -------------------------------- |
| game_id        | INTEGER   | Unique game identifier           |
| white_id       | TEXT      | White player's username          |
| black_id       | TEXT      | Black player's username          |
| winner         | TEXT      | Game winner (White, Black, Draw) |
| victory_status | TEXT      | Method of victory                |
| turns          | INTEGER   | Number of turns played           |
| time_increment | TEXT      | Time control format              |
| rated          | INTEGER   | Rated game flag (0 or 1)         |
| opening_code   | TEXT      | Opening used in the game         |
| white_rating   | INTEGER   | White player's rating            |
| black_rating   | INTEGER   | Black player's rating            |

### Primary Key

* game_id

### Foreign Keys

#### white_id → players.username

Links every game to the player who played the white pieces. This relationship allows player statistics, rankings, and historical performance analysis.

#### black_id → players.username

Links every game to the player who played the black pieces. This enables player-based analytics from either side of the board.

#### opening_code → openings.opening_code

Connects each game to a standardized opening definition. This avoids storing opening names repeatedly and allows efficient opening analysis.

---

# Database Relationships

players (1) ────────< games >──────── (1) openings

A single player can participate in many games.

A single opening can appear in many games.

Each game references exactly one opening and two players.

---

# Data Integrity

The database enforces several constraints:

* PRIMARY KEY constraints ensure uniqueness.
* FOREIGN KEY constraints guarantee valid player and opening references.
* CHECK constraints validate winner values (White, Black, Draw).
* CHECK constraints ensure turns are greater than zero.
* NOT NULL constraints prevent missing critical information.

These constraints help maintain a clean, reliable, and production-quality analytical database.

---

# How to Run the Project

## Requirements

Before running the project, make sure you have:

* Python 3.10 or newer
* Required Python packages installed

Install dependencies using:

```bash
pip install -r requirements.txt
```

---

## Running the Database Pipeline

From the project root directory, execute:

```bash
python -m src.db
```

This command will:

1. Load the chess dataset.
2. Create and populate the SQLite database.
3. Validate the database schema and constraints.
4. Create indexes for query optimization.
5. Execute all required SQL queries.
6. Run the extended analytical queries.
7. Generate feature-engineering outputs.

---

# Expected Output

When the pipeline runs successfully, the terminal will display:

* Dataset loading information.
* Results for Stage 1 (SELECT queries).
* Results for Stage 2 (GROUP BY queries).
* Results for Stage 3 (JOINs and CTEs).
* Results for Stage 4 (Window Functions).
* Query plan output showing index usage.
* Results for all extended SQL analyses.

Example:

```text
=== CHESS DATABASE PIPELINE ===

Loaded dataset: 20,058 rows

============================================================
STAGE 1 - SELECT
============================================================

Q1
...
```

---

# Generated Files

After execution, the following files are produced:

### SQLite Database

```text
data/chess.db
```

Contains the normalized database with all tables, relationships, indexes, and loaded data.

### Feature Table

```text
data/processed/features.csv
```

Contains engineered features derived from the chess games dataset for further analysis or machine learning tasks.

### Window Function Output

```text
data/processed/game_ranks.csv
```

Contains ranking results generated using SQL window functions.

---

# Project Outputs Summary

Running the project successfully will produce:

* A fully populated SQLite database.
* Validated relational schema.
* Indexed tables for faster queries.
* SQL analysis results printed to the console.
* Feature engineering dataset (`features.csv`).
* Ranking dataset (`game_ranks.csv`).

These outputs demonstrate database design, SQL querying, optimization using indexes, and analytical reporting on chess game data.
