"""
BeePower Stok Takip Sistemi - Veritabanı Katmanı
Database layer for BeePower Stock Tracking System
"""
from __future__ import annotations

import sqlite3
import os
from datetime import datetime
from typing import Optional


DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "beepower_stock.db")


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def initialize_db():
    """Create all tables if they don't exist."""
    conn = get_connection()
    cursor = conn.cursor()

    # ── Robots table ─────────────────────────────────────────────────────────
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS robots (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            name        TEXT    NOT NULL UNIQUE,
            model       TEXT,
            serial_no   TEXT,
            description TEXT,
            created_at  TEXT    NOT NULL DEFAULT (datetime('now','localtime'))
        )
    """)

    # ── Module categories ─────────────────────────────────────────────────────
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS module_categories (
            id   INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT    NOT NULL UNIQUE
        )
    """)

    # ── Inventory modules ─────────────────────────────────────────────────────
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS inventory (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            module_id    TEXT    NOT NULL UNIQUE,
            name         TEXT    NOT NULL,
            category_id  INTEGER REFERENCES module_categories(id),
            quantity     INTEGER NOT NULL DEFAULT 0,
            status       TEXT    NOT NULL DEFAULT 'available'
                                 CHECK(status IN ('available','faulty','unusable')),
            description  TEXT,
            supplier     TEXT,
            unit_cost    REAL,
            location     TEXT,
            created_at   TEXT    NOT NULL DEFAULT (datetime('now','localtime')),
            updated_at   TEXT    NOT NULL DEFAULT (datetime('now','localtime'))
        )
    """)

    # ── Maintenance / change records ──────────────────────────────────────────
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS records (
            id                  INTEGER PRIMARY KEY AUTOINCREMENT,
            robot_id            INTEGER NOT NULL REFERENCES robots(id),
            module_category     TEXT,
            old_module_id       TEXT,
            old_module_name     TEXT,
            reason              TEXT    NOT NULL,
            solution            TEXT    NOT NULL,
            new_module_id       TEXT    REFERENCES inventory(module_id),
            record_date         TEXT    NOT NULL,
            technician          TEXT,
            duration_minutes    INTEGER,
            cost                REAL,
            description         TEXT,
            status              TEXT    NOT NULL DEFAULT 'completed'
                                        CHECK(status IN ('completed','pending','in_progress')),
            created_at          TEXT    NOT NULL DEFAULT (datetime('now','localtime'))
        )
    """)

    # ── Seed some default module categories ───────────────────────────────────
    default_categories = [
        "Tekerlek / Wheel",
        "Motor / Motor",
        "Sensör / Sensor",
        "Kontrol Kartı / Control Board",
        "Pil / Battery",
        "Kablo / Cable",
        "Yapı / Frame",
        "Diğer / Other",
    ]
    for cat in default_categories:
        cursor.execute(
            "INSERT OR IGNORE INTO module_categories(name) VALUES(?)", (cat,)
        )

    conn.commit()
    conn.close()


# ═══════════════════════════════════════════════════════════════════════════════
#  ROBOTS
# ═══════════════════════════════════════════════════════════════════════════════

def get_all_robots() -> list[dict]:
    conn = get_connection()
    rows = conn.execute("SELECT * FROM robots ORDER BY name").fetchall()
    conn.close()
    return [dict(r) for r in rows]


def add_robot(name: str, model: str = "", serial_no: str = "", description: str = "") -> int:
    conn = get_connection()
    cur = conn.execute(
        "INSERT INTO robots(name, model, serial_no, description) VALUES(?,?,?,?)",
        (name, model, serial_no, description),
    )
    conn.commit()
    row_id = cur.lastrowid
    conn.close()
    return row_id


def update_robot(robot_id: int, name: str, model: str, serial_no: str, description: str):
    conn = get_connection()
    conn.execute(
        "UPDATE robots SET name=?, model=?, serial_no=?, description=? WHERE id=?",
        (name, model, serial_no, description, robot_id),
    )
    conn.commit()
    conn.close()


def delete_robot(robot_id: int):
    conn = get_connection()
    conn.execute("DELETE FROM robots WHERE id=?", (robot_id,))
    conn.commit()
    conn.close()


# ═══════════════════════════════════════════════════════════════════════════════
#  INVENTORY
# ═══════════════════════════════════════════════════════════════════════════════

def get_all_inventory(status: Optional[str] = None) -> list[dict]:
    conn = get_connection()
    if status:
        rows = conn.execute(
            """SELECT i.*, mc.name as category_name
               FROM inventory i
               LEFT JOIN module_categories mc ON i.category_id = mc.id
               WHERE i.status = ?
               ORDER BY i.name""",
            (status,),
        ).fetchall()
    else:
        rows = conn.execute(
            """SELECT i.*, mc.name as category_name
               FROM inventory i
               LEFT JOIN module_categories mc ON i.category_id = mc.id
               ORDER BY i.name"""
        ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_inventory_by_module_id(module_id: str) -> Optional[dict]:
    conn = get_connection()
    row = conn.execute(
        "SELECT * FROM inventory WHERE module_id=?", (module_id,)
    ).fetchone()
    conn.close()
    return dict(row) if row else None


def add_inventory(
    module_id: str,
    name: str,
    category_id: Optional[int],
    quantity: int,
    status: str,
    description: str = "",
    supplier: str = "",
    unit_cost: Optional[float] = None,
    location: str = "",
) -> int:
    conn = get_connection()
    cur = conn.execute(
        """INSERT INTO inventory
           (module_id, name, category_id, quantity, status, description, supplier, unit_cost, location)
           VALUES(?,?,?,?,?,?,?,?,?)""",
        (module_id, name, category_id, quantity, status, description, supplier, unit_cost, location),
    )
    conn.commit()
    row_id = cur.lastrowid
    conn.close()
    return row_id


def update_inventory(
    inv_id: int,
    module_id: str,
    name: str,
    category_id: Optional[int],
    quantity: int,
    status: str,
    description: str = "",
    supplier: str = "",
    unit_cost: Optional[float] = None,
    location: str = "",
):
    conn = get_connection()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn.execute(
        """UPDATE inventory SET
           module_id=?, name=?, category_id=?, quantity=?, status=?,
           description=?, supplier=?, unit_cost=?, location=?, updated_at=?
           WHERE id=?""",
        (module_id, name, category_id, quantity, status, description, supplier, unit_cost, location, now, inv_id),
    )
    conn.commit()
    conn.close()


def update_inventory_status(module_id: str, new_status: str):
    conn = get_connection()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn.execute(
        "UPDATE inventory SET status=?, updated_at=? WHERE module_id=?",
        (new_status, now, module_id),
    )
    conn.commit()
    conn.close()


def delete_inventory(inv_id: int):
    conn = get_connection()
    conn.execute("DELETE FROM inventory WHERE id=?", (inv_id,))
    conn.commit()
    conn.close()


def search_inventory(query: str) -> list[dict]:
    conn = get_connection()
    like = f"%{query}%"
    rows = conn.execute(
        """SELECT i.*, mc.name as category_name
           FROM inventory i
           LEFT JOIN module_categories mc ON i.category_id = mc.id
           WHERE i.module_id LIKE ? OR i.name LIKE ? OR i.description LIKE ?
           ORDER BY i.name""",
        (like, like, like),
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


# ═══════════════════════════════════════════════════════════════════════════════
#  RECORDS
# ═══════════════════════════════════════════════════════════════════════════════

def get_all_records(robot_id: Optional[int] = None) -> list[dict]:
    conn = get_connection()
    if robot_id:
        rows = conn.execute(
            """SELECT r.*, rb.name as robot_name
               FROM records r
               JOIN robots rb ON r.robot_id = rb.id
               WHERE r.robot_id = ?
               ORDER BY r.record_date DESC""",
            (robot_id,),
        ).fetchall()
    else:
        rows = conn.execute(
            """SELECT r.*, rb.name as robot_name
               FROM records r
               JOIN robots rb ON r.robot_id = rb.id
               ORDER BY r.record_date DESC"""
        ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def add_record(
    robot_id: int,
    module_category: str,
    old_module_id: str,
    old_module_name: str,
    reason: str,
    solution: str,
    new_module_id: str,
    record_date: str,
    technician: str = "",
    duration_minutes: Optional[int] = None,
    cost: Optional[float] = None,
    description: str = "",
    status: str = "completed",
) -> int:
    conn = get_connection()
    cur = conn.execute(
        """INSERT INTO records
           (robot_id, module_category, old_module_id, old_module_name, reason, solution,
            new_module_id, record_date, technician, duration_minutes, cost, description, status)
           VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)""",
        (
            robot_id, module_category, old_module_id, old_module_name, reason, solution,
            new_module_id, record_date, technician, duration_minutes, cost, description, status,
        ),
    )
    conn.commit()
    row_id = cur.lastrowid
    conn.close()
    return row_id


def update_record(
    rec_id: int,
    robot_id: int,
    module_category: str,
    old_module_id: str,
    old_module_name: str,
    reason: str,
    solution: str,
    new_module_id: str,
    record_date: str,
    technician: str = "",
    duration_minutes: Optional[int] = None,
    cost: Optional[float] = None,
    description: str = "",
    status: str = "completed",
):
    conn = get_connection()
    conn.execute(
        """UPDATE records SET
           robot_id=?, module_category=?, old_module_id=?, old_module_name=?,
           reason=?, solution=?, new_module_id=?, record_date=?, technician=?,
           duration_minutes=?, cost=?, description=?, status=?
           WHERE id=?""",
        (
            robot_id, module_category, old_module_id, old_module_name, reason, solution,
            new_module_id, record_date, technician, duration_minutes, cost, description, status,
            rec_id,
        ),
    )
    conn.commit()
    conn.close()


def delete_record(rec_id: int):
    conn = get_connection()
    conn.execute("DELETE FROM records WHERE id=?", (rec_id,))
    conn.commit()
    conn.close()


def search_records(query: str) -> list[dict]:
    conn = get_connection()
    like = f"%{query}%"
    rows = conn.execute(
        """SELECT r.*, rb.name as robot_name
           FROM records r
           JOIN robots rb ON r.robot_id = rb.id
           WHERE rb.name LIKE ? OR r.module_category LIKE ? OR r.old_module_id LIKE ?
              OR r.reason LIKE ? OR r.description LIKE ? OR r.technician LIKE ?
           ORDER BY r.record_date DESC""",
        (like, like, like, like, like, like),
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


# ═══════════════════════════════════════════════════════════════════════════════
#  CATEGORIES
# ═══════════════════════════════════════════════════════════════════════════════

def get_all_categories() -> list[dict]:
    conn = get_connection()
    rows = conn.execute("SELECT * FROM module_categories ORDER BY name").fetchall()
    conn.close()
    return [dict(r) for r in rows]


def add_category(name: str) -> int:
    conn = get_connection()
    cur = conn.execute("INSERT OR IGNORE INTO module_categories(name) VALUES(?)", (name,))
    conn.commit()
    row_id = cur.lastrowid
    conn.close()
    return row_id


# ═══════════════════════════════════════════════════════════════════════════════
#  STATS / DASHBOARD
# ═══════════════════════════════════════════════════════════════════════════════

def get_dashboard_stats() -> dict:
    conn = get_connection()
    stats = {}
    stats["total_robots"]     = conn.execute("SELECT COUNT(*) FROM robots").fetchone()[0]
    stats["total_records"]    = conn.execute("SELECT COUNT(*) FROM records").fetchone()[0]
    stats["total_modules"]    = conn.execute("SELECT COUNT(*) FROM inventory").fetchone()[0]
    stats["available_count"]  = conn.execute("SELECT COUNT(*) FROM inventory WHERE status='available'").fetchone()[0]
    stats["faulty_count"]     = conn.execute("SELECT COUNT(*) FROM inventory WHERE status='faulty'").fetchone()[0]
    stats["unusable_count"]   = conn.execute("SELECT COUNT(*) FROM inventory WHERE status='unusable'").fetchone()[0]
    stats["recent_records"]   = [
        dict(r) for r in conn.execute(
            """SELECT r.*, rb.name as robot_name
               FROM records r JOIN robots rb ON r.robot_id=rb.id
               ORDER BY r.record_date DESC LIMIT 5"""
        ).fetchall()
    ]
    conn.close()
    return stats
