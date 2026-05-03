"""
Initialize the BallPark Lab SQLite database with seed data.

Run from the project root:
    python scripts/init_db.py
"""
from __future__ import annotations

import hashlib
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
DB_PATH = BASE_DIR / "ballpark.db"


def weak_password_hash(password: str) -> str:
    """Intentionally simple hash for the vulnerable lab version."""
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def main() -> None:
    if DB_PATH.exists():
        DB_PATH.unlink()

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.executescript(
        """
        PRAGMA foreign_keys = ON;

        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'user',
            favorite_team_id INTEGER,
            points INTEGER NOT NULL DEFAULT 10000,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE teams (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            home_city TEXT NOT NULL
        );

        CREATE TABLE games (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            home_team_id INTEGER NOT NULL,
            away_team_id INTEGER NOT NULL,
            game_date TEXT NOT NULL,
            stadium TEXT NOT NULL,
            home_score INTEGER,
            away_score INTEGER,
            status TEXT NOT NULL DEFAULT 'scheduled',
            FOREIGN KEY (home_team_id) REFERENCES teams(id),
            FOREIGN KEY (away_team_id) REFERENCES teams(id)
        );

        CREATE TABLE comments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            game_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            content TEXT NOT NULL,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (game_id) REFERENCES games(id),
            FOREIGN KEY (user_id) REFERENCES users(id)
        );

        CREATE TABLE attendance_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            game_id INTEGER NOT NULL,
            seat_section TEXT NOT NULL,
            memo TEXT,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (game_id) REFERENCES games(id)
        );

        CREATE TABLE point_transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            amount INTEGER NOT NULL,
            reason TEXT NOT NULL,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        );

        CREATE TABLE ticket_reservations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            game_id INTEGER NOT NULL,
            seat_no TEXT NOT NULL,
            paid_points INTEGER NOT NULL,
            status TEXT NOT NULL DEFAULT 'reserved',
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (game_id) REFERENCES games(id)
        );
        """
    )

    teams = [
        ("Seoul Bears", "Seoul"),
        ("Busan Giants", "Busan"),
        ("Incheon Landers", "Incheon"),
        ("Daegu Lions", "Daegu"),
    ]
    cur.executemany("INSERT INTO teams (name, home_city) VALUES (?, ?)", teams)

    games = [
        (1, 2, "2026-05-10 18:30", "Jamsil Baseball Stadium", None, None, "scheduled"),
        (3, 4, "2026-05-10 18:30", "Incheon Ballpark", None, None, "scheduled"),
        (2, 1, "2026-05-11 14:00", "Busan Ballpark", 5, 3, "final"),
    ]
    cur.executemany(
        """
        INSERT INTO games
        (home_team_id, away_team_id, game_date, stadium, home_score, away_score, status)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        games,
    )

    users = [
        ("alice", weak_password_hash("alice1234"), "user", 1, 12000),
        ("bob", weak_password_hash("bob1234"), "user", 2, 9000),
        ("admin", weak_password_hash("admin1234"), "admin", 1, 50000),
    ]
    cur.executemany(
        """
        INSERT INTO users (username, password_hash, role, favorite_team_id, points)
        VALUES (?, ?, ?, ?, ?)
        """,
        users,
    )

    attendance = [
        (1, 1, "1B-101", "Opening week game"),
        (2, 3, "3B-205", "Away win memory"),
    ]
    cur.executemany(
        """
        INSERT INTO attendance_records (user_id, game_id, seat_section, memo)
        VALUES (?, ?, ?, ?)
        """,
        attendance,
    )

    conn.commit()
    conn.close()
    print(f"Initialized database: {DB_PATH}")
    print("Seed users:")
    print("  alice / alice1234 / role=user")
    print("  bob   / bob1234   / role=user")
    print("  admin / admin1234 / role=admin")


if __name__ == "__main__":
    main()
