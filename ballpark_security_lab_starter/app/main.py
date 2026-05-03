"""
BallPark Lab - intentionally vulnerable Web/API service for a local security-assessment portfolio.

This application is for your own local lab only. It contains deliberate weaknesses so that you
can practice: finding, documenting, fixing, and retesting vulnerabilities.
"""
from __future__ import annotations

import base64
import hashlib
import hmac
import json
import os
import sqlite3
from pathlib import Path
from typing import Any

from fastapi import Depends, FastAPI, File, Header, HTTPException, UploadFile
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

BASE_DIR = Path(__file__).resolve().parents[1]
DB_PATH = BASE_DIR / "ballpark.db"
UPLOAD_DIR = BASE_DIR / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)

# INTENTIONAL LAB WEAKNESS:
# The signing secret is hardcoded. In the secure version, move it to an environment variable.
TOKEN_SECRET = "ballpark-lab-hardcoded-secret"

app = FastAPI(
    title="BallPark Lab API",
    description="A baseball fan community and ticket simulation service for security testing.",
    version="0.1.0-vulnerable",
)


class RegisterRequest(BaseModel):
    username: str = Field(min_length=3, max_length=32)
    password: str = Field(min_length=4, max_length=128)
    favorite_team_id: int | None = None


class LoginRequest(BaseModel):
    username: str
    password: str


class CommentRequest(BaseModel):
    content: str = Field(min_length=1, max_length=2000)


class AttendanceRequest(BaseModel):
    game_id: int
    seat_section: str
    memo: str | None = None


class ChargeRequest(BaseModel):
    amount: int
    reason: str = "manual-charge"


class TicketReservationRequest(BaseModel):
    game_id: int
    seat_no: str
    client_price: int


class AdminGameUpdateRequest(BaseModel):
    home_score: int | None = None
    away_score: int | None = None
    status: str | None = None


def db() -> sqlite3.Connection:
    if not DB_PATH.exists():
        raise HTTPException(
            status_code=500,
            detail="Database not initialized. Run: python scripts/init_db.py",
        )
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def row_to_dict(row: sqlite3.Row | None) -> dict[str, Any] | None:
    if row is None:
        return None
    return dict(row)


def weak_password_hash(password: str) -> str:
    # INTENTIONAL LAB WEAKNESS:
    # SHA-256 without salt is not appropriate for password storage.
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def b64url_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).decode("utf-8").rstrip("=")


def b64url_decode(data: str) -> bytes:
    padding = "=" * (-len(data) % 4)
    return base64.urlsafe_b64decode(data + padding)


def create_demo_token(user: dict[str, Any]) -> str:
    payload = {
        "user_id": user["id"],
        "username": user["username"],
        "role": user["role"],
    }
    payload_part = b64url_encode(json.dumps(payload, separators=(",", ":")).encode("utf-8"))
    signature = hmac.new(
        TOKEN_SECRET.encode("utf-8"),
        payload_part.encode("utf-8"),
        hashlib.sha256,
    ).digest()
    return f"{payload_part}.{b64url_encode(signature)}"


def verify_demo_token(token: str) -> dict[str, Any]:
    try:
        payload_part, signature_part = token.split(".", maxsplit=1)
        expected = hmac.new(
            TOKEN_SECRET.encode("utf-8"),
            payload_part.encode("utf-8"),
            hashlib.sha256,
        ).digest()
        actual = b64url_decode(signature_part)
        if not hmac.compare_digest(expected, actual):
            raise ValueError("bad signature")
        payload = json.loads(b64url_decode(payload_part))
        return payload
    except Exception as exc:  # noqa: BLE001 - return a generic auth error to clients
        raise HTTPException(status_code=401, detail="Invalid token") from exc


def get_current_user(authorization: str | None = Header(default=None)) -> dict[str, Any]:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing Bearer token")

    token = authorization.removeprefix("Bearer ").strip()
    payload = verify_demo_token(token)

    conn = db()
    try:
        user = conn.execute(
            "SELECT id, username, role, favorite_team_id, points FROM users WHERE id = ?",
            (payload["user_id"],),
        ).fetchone()
    finally:
        conn.close()

    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return dict(user)


@app.get("/")
def index() -> dict[str, Any]:
    return {
        "service": "BallPark Lab",
        "version": "0.1.0-vulnerable",
        "next_steps": [
            "Run python scripts/init_db.py if the database is missing.",
            "Open /docs for the OpenAPI UI.",
            "Use /auth/login with alice/alice1234, bob/bob1234, or admin/admin1234.",
            "Open /games/1/page to view a simple HTML game page.",
        ],
    }


@app.post("/auth/register")
def register(body: RegisterRequest) -> dict[str, Any]:
    conn = db()
    try:
        cur = conn.execute(
            """
            INSERT INTO users (username, password_hash, role, favorite_team_id, points)
            VALUES (?, ?, 'user', ?, 10000)
            """,
            (body.username, weak_password_hash(body.password), body.favorite_team_id),
        )
        conn.commit()
        user_id = cur.lastrowid
        return {"id": user_id, "username": body.username, "role": "user"}
    except sqlite3.IntegrityError as exc:
        raise HTTPException(status_code=409, detail="Username already exists") from exc
    finally:
        conn.close()


@app.post("/auth/login")
def login(body: LoginRequest) -> dict[str, Any]:
    conn = db()
    try:
        user = conn.execute(
            "SELECT id, username, password_hash, role, favorite_team_id, points FROM users WHERE username = ?",
            (body.username,),
        ).fetchone()
    finally:
        conn.close()

    if user is None or user["password_hash"] != weak_password_hash(body.password):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    user_dict = dict(user)
    return {
        "access_token": create_demo_token(user_dict),
        "token_type": "bearer",
        "user": {
            "id": user_dict["id"],
            "username": user_dict["username"],
            "role": user_dict["role"],
            "points": user_dict["points"],
        },
    }


@app.get("/api/me")
def me(current_user: dict[str, Any] = Depends(get_current_user)) -> dict[str, Any]:
    return current_user


@app.get("/api/teams")
def list_teams() -> list[dict[str, Any]]:
    conn = db()
    try:
        rows = conn.execute("SELECT id, name, home_city FROM teams ORDER BY id").fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()


@app.get("/api/games")
def list_games() -> list[dict[str, Any]]:
    conn = db()
    try:
        rows = conn.execute(
            """
            SELECT
                g.id,
                g.game_date,
                g.stadium,
                g.home_score,
                g.away_score,
                g.status,
                ht.name AS home_team,
                at.name AS away_team
            FROM games g
            JOIN teams ht ON ht.id = g.home_team_id
            JOIN teams at ON at.id = g.away_team_id
            ORDER BY g.game_date ASC
            """
        ).fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()


@app.get("/api/games/{game_id}")
def get_game(game_id: int) -> dict[str, Any]:
    conn = db()
    try:
        game = conn.execute(
            """
            SELECT
                g.id,
                g.game_date,
                g.stadium,
                g.home_score,
                g.away_score,
                g.status,
                ht.name AS home_team,
                at.name AS away_team
            FROM games g
            JOIN teams ht ON ht.id = g.home_team_id
            JOIN teams at ON at.id = g.away_team_id
            WHERE g.id = ?
            """,
            (game_id,),
        ).fetchone()
        if game is None:
            raise HTTPException(status_code=404, detail="Game not found")
        return dict(game)
    finally:
        conn.close()


@app.post("/api/games/{game_id}/comments")
def create_comment(
    game_id: int,
    body: CommentRequest,
    current_user: dict[str, Any] = Depends(get_current_user),
) -> dict[str, Any]:
    # INTENTIONAL LAB WEAKNESS:
    # Content is stored without sanitization. The HTML page below also renders it unsafely.
    conn = db()
    try:
        cur = conn.execute(
            "INSERT INTO comments (game_id, user_id, content) VALUES (?, ?, ?)",
            (game_id, current_user["id"], body.content),
        )
        conn.commit()
        return {"id": cur.lastrowid, "game_id": game_id, "content": body.content}
    finally:
        conn.close()


@app.get("/api/games/{game_id}/comments")
def list_comments(game_id: int) -> list[dict[str, Any]]:
    conn = db()
    try:
        rows = conn.execute(
            """
            SELECT c.id, c.content, c.created_at, u.username
            FROM comments c
            JOIN users u ON u.id = c.user_id
            WHERE c.game_id = ?
            ORDER BY c.id DESC
            """,
            (game_id,),
        ).fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()


@app.get("/games/{game_id}/page", response_class=HTMLResponse)
def game_page(game_id: int) -> str:
    """Simple HTML page for XSS assessment in a local lab."""
    conn = db()
    try:
        game = conn.execute(
            """
            SELECT g.id, g.game_date, g.stadium, ht.name AS home_team, at.name AS away_team
            FROM games g
            JOIN teams ht ON ht.id = g.home_team_id
            JOIN teams at ON at.id = g.away_team_id
            WHERE g.id = ?
            """,
            (game_id,),
        ).fetchone()
        if game is None:
            raise HTTPException(status_code=404, detail="Game not found")

        comments = conn.execute(
            """
            SELECT c.content, c.created_at, u.username
            FROM comments c
            JOIN users u ON u.id = c.user_id
            WHERE c.game_id = ?
            ORDER BY c.id DESC
            """,
            (game_id,),
        ).fetchall()
    finally:
        conn.close()

    # INTENTIONAL LAB WEAKNESS:
    # The comment content is concatenated directly into HTML without escaping.
    comments_html = "".join(
        f"<li><b>{row['username']}</b>: {row['content']} <small>{row['created_at']}</small></li>"
        for row in comments
    )
    return f"""
    <!doctype html>
    <html lang="ko">
      <head><meta charset="utf-8"><title>BallPark Game</title></head>
      <body>
        <h1>{game['away_team']} vs {game['home_team']}</h1>
        <p>{game['game_date']} / {game['stadium']}</p>
        <h2>Fan comments</h2>
        <ul>{comments_html}</ul>
        <p>Use POST /api/games/{game_id}/comments to add comments.</p>
      </body>
    </html>
    """


@app.post("/api/attendance")
def create_attendance(
    body: AttendanceRequest,
    current_user: dict[str, Any] = Depends(get_current_user),
) -> dict[str, Any]:
    conn = db()
    try:
        cur = conn.execute(
            """
            INSERT INTO attendance_records (user_id, game_id, seat_section, memo)
            VALUES (?, ?, ?, ?)
            """,
            (current_user["id"], body.game_id, body.seat_section, body.memo),
        )
        conn.commit()
        return {"id": cur.lastrowid, "message": "Attendance record created"}
    finally:
        conn.close()


@app.get("/api/users/{user_id}/attendance")
def list_user_attendance(
    user_id: int,
    current_user: dict[str, Any] = Depends(get_current_user),
) -> list[dict[str, Any]]:
    # INTENTIONAL LAB WEAKNESS:
    # Any authenticated user can request another user's attendance records by changing user_id.
    _ = current_user
    conn = db()
    try:
        rows = conn.execute(
            """
            SELECT ar.id, ar.user_id, ar.game_id, ar.seat_section, ar.memo, ar.created_at,
                   ht.name AS home_team, at.name AS away_team
            FROM attendance_records ar
            JOIN games g ON g.id = ar.game_id
            JOIN teams ht ON ht.id = g.home_team_id
            JOIN teams at ON at.id = g.away_team_id
            WHERE ar.user_id = ?
            ORDER BY ar.id DESC
            """,
            (user_id,),
        ).fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()


@app.post("/api/points/charge")
def charge_points(
    body: ChargeRequest,
    current_user: dict[str, Any] = Depends(get_current_user),
) -> dict[str, Any]:
    # INTENTIONAL LAB WEAKNESS:
    # The server does not validate allowed amount ranges or business rules.
    conn = db()
    try:
        conn.execute(
            "UPDATE users SET points = points + ? WHERE id = ?",
            (body.amount, current_user["id"]),
        )
        conn.execute(
            "INSERT INTO point_transactions (user_id, amount, reason) VALUES (?, ?, ?)",
            (current_user["id"], body.amount, body.reason),
        )
        conn.commit()
        updated = conn.execute("SELECT points FROM users WHERE id = ?", (current_user["id"],)).fetchone()
        return {"message": "points charged", "points": updated["points"]}
    finally:
        conn.close()


@app.post("/api/tickets/reserve")
def reserve_ticket(
    body: TicketReservationRequest,
    current_user: dict[str, Any] = Depends(get_current_user),
) -> dict[str, Any]:
    # INTENTIONAL LAB WEAKNESSES:
    # 1. The server trusts client_price instead of calculating price server-side.
    # 2. The server does not check whether the same seat is already reserved.
    # 3. There is no idempotency key or transaction-level business validation.
    conn = db()
    try:
        user = conn.execute("SELECT points FROM users WHERE id = ?", (current_user["id"],)).fetchone()
        if user is None:
            raise HTTPException(status_code=401, detail="User not found")

        if user["points"] < body.client_price:
            raise HTTPException(status_code=400, detail="Not enough points")

        conn.execute(
            "UPDATE users SET points = points - ? WHERE id = ?",
            (body.client_price, current_user["id"]),
        )
        cur = conn.execute(
            """
            INSERT INTO ticket_reservations (user_id, game_id, seat_no, paid_points)
            VALUES (?, ?, ?, ?)
            """,
            (current_user["id"], body.game_id, body.seat_no, body.client_price),
        )
        conn.commit()
        return {"reservation_id": cur.lastrowid, "message": "reserved"}
    finally:
        conn.close()


@app.get("/api/tickets/me")
def my_tickets(current_user: dict[str, Any] = Depends(get_current_user)) -> list[dict[str, Any]]:
    conn = db()
    try:
        rows = conn.execute(
            """
            SELECT id, game_id, seat_no, paid_points, status, created_at
            FROM ticket_reservations
            WHERE user_id = ?
            ORDER BY id DESC
            """,
            (current_user["id"],),
        ).fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()


@app.put("/api/admin/games/{game_id}")
def admin_update_game(
    game_id: int,
    body: AdminGameUpdateRequest,
    current_user: dict[str, Any] = Depends(get_current_user),
) -> dict[str, Any]:
    # INTENTIONAL LAB WEAKNESS:
    # This endpoint should require role == 'admin', but currently any logged-in user can update a game.
    _ = current_user
    fields: list[str] = []
    values: list[Any] = []
    if body.home_score is not None:
        fields.append("home_score = ?")
        values.append(body.home_score)
    if body.away_score is not None:
        fields.append("away_score = ?")
        values.append(body.away_score)
    if body.status is not None:
        fields.append("status = ?")
        values.append(body.status)

    if not fields:
        raise HTTPException(status_code=400, detail="No fields to update")

    values.append(game_id)
    conn = db()
    try:
        cur = conn.execute(f"UPDATE games SET {', '.join(fields)} WHERE id = ?", values)
        conn.commit()
        if cur.rowcount == 0:
            raise HTTPException(status_code=404, detail="Game not found")
        return {"message": "game updated"}
    finally:
        conn.close()


@app.post("/api/profile/upload")
def upload_profile_image(
    file: UploadFile = File(...),
    current_user: dict[str, Any] = Depends(get_current_user),
) -> dict[str, Any]:
    # INTENTIONAL LAB WEAKNESS:
    # This stores user-controlled files with only minimal filename normalization.
    # The secure version should validate size, extension, MIME type, storage location, and scanning policy.
    original_name = os.path.basename(file.filename or "uploaded.bin")
    save_name = f"user_{current_user['id']}_{original_name}"
    save_path = UPLOAD_DIR / save_name

    with save_path.open("wb") as out:
        out.write(file.file.read())

    return {"message": "uploaded", "filename": save_name, "path": str(save_path)}
