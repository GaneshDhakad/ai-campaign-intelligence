"""
SQLite Database Connection Manager
"""
import sqlite3
import os
import json
from datetime import datetime
from contextlib import contextmanager

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data', 'campaign_engine.db')


@contextmanager
def get_connection():
    """Thread-safe SQLite connection context manager."""
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def init_db():
    """Create tables if they don't exist."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

    with get_connection() as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS predictions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                input_json TEXT NOT NULL,
                prediction TEXT NOT NULL,
                probability REAL NOT NULL,
                risk_level TEXT,
                recommendation TEXT,
                sentiment_label INTEGER,
                segment_id INTEGER
            );

            CREATE TABLE IF NOT EXISTS sentiment_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                text TEXT NOT NULL,
                label INTEGER,
                compound REAL,
                confidence REAL,
                intensity TEXT
            );

            CREATE TABLE IF NOT EXISTS batch_jobs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                filename TEXT,
                total_records INTEGER,
                avg_probability REAL,
                respond_count INTEGER
            );

            CREATE INDEX IF NOT EXISTS idx_pred_ts ON predictions(timestamp);
            CREATE INDEX IF NOT EXISTS idx_sent_ts ON sentiment_logs(timestamp);
        """)
    print("  ✓ Database initialized")


def store_prediction(input_data: dict, result: dict, sentiment_label=None, segment_id=None):
    """Store a prediction result."""
    with get_connection() as conn:
        conn.execute(
            """INSERT INTO predictions (timestamp, input_json, prediction, probability,
               risk_level, recommendation, sentiment_label, segment_id)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (datetime.now().isoformat(), json.dumps(input_data), result['prediction'],
             float(result['probability']), result['risk_level'], result['recommendation'],
             sentiment_label, segment_id)
        )


def store_sentiment(text: str, result: dict):
    """Store a sentiment analysis result."""
    with get_connection() as conn:
        conn.execute(
            """INSERT INTO sentiment_logs (timestamp, text, label, compound, confidence, intensity)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (datetime.now().isoformat(), text[:500], result['label'],
             float(result['compound']), float(result['confidence']), result['intensity'])
        )


def store_batch_job(filename: str, total: int, avg_prob: float, respond_count: int):
    """Store batch job metadata."""
    with get_connection() as conn:
        conn.execute(
            """INSERT INTO batch_jobs (timestamp, filename, total_records, avg_probability, respond_count)
               VALUES (?, ?, ?, ?, ?)""",
            (datetime.now().isoformat(), filename, total, float(avg_prob), respond_count)
        )


def get_prediction_history(limit=100):
    """Fetch recent predictions."""
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT * FROM predictions ORDER BY timestamp DESC LIMIT ?", (limit,)
        ).fetchall()
        return [dict(r) for r in rows]


def get_analytics_summary():
    """Get aggregate analytics."""
    with get_connection() as conn:
        total = conn.execute("SELECT COUNT(*) as c FROM predictions").fetchone()['c']
        avg_prob = conn.execute("SELECT AVG(probability) as a FROM predictions").fetchone()['a'] or 0
        respond = conn.execute(
            "SELECT COUNT(*) as c FROM predictions WHERE prediction = 'Will Respond'"
        ).fetchone()['c']
        sent_total = conn.execute("SELECT COUNT(*) as c FROM sentiment_logs").fetchone()['c']
        avg_compound = conn.execute(
            "SELECT AVG(compound) as a FROM sentiment_logs"
        ).fetchone()['a'] or 0

        return {
            'total_predictions': total,
            'avg_probability': round(avg_prob, 2),
            'respond_rate': round(respond / total * 100, 1) if total > 0 else 0,
            'total_sentiments': sent_total,
            'avg_sentiment': round(avg_compound, 4)
        }
