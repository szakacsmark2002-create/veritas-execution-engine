import psycopg2
from psycopg2.extras import RealDictCursor, Json
from uuid import uuid4
from datetime import datetime



DB_NAME = "saco_db"
DB_USER = "mark_yfx"
DB_HOST = "localhost"
DB_PORT = 5432


def get_connection():
    return psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        host=DB_HOST,
        port=DB_PORT
    )


def get_previous_execution_hash():

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT execution_hash FROM executions ORDER BY sequence_number DESC LIMIT 1;"
    )

    row = cur.fetchone()

    cur.close()
    conn.close()

    if row:
        return row[0]
    return None


def insert_execution(record: dict, previous_hash: str | None):

    conn = get_connection()
    cur = conn.cursor()

    execution_id = str(uuid4())
    ts_utc = datetime.utcnow()

    cur.execute("""
        INSERT INTO executions (
            execution_id,
            ts_utc,
            engine_version,
            schema_version,
            previous_execution_hash,
            input_hash,
            world_hash,
            result_hash,
            execution_hash,
            input_json,
            world_json,
            result_json
        )
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """, (
        execution_id,
        ts_utc,
        record["engine_version"],
        record["schema_version"],
        previous_hash,
        record["input_hash"],
        record["world_hash"],
        record["result_hash"],
        record["execution_hash"],
        Json(record["input"]),
        Json(record["world"]),
        Json(record["result"])
    ))

    conn.commit()
    cur.close()
    conn.close()

    return execution_id
from psycopg2.extras import RealDictCursor


def get_execution_by_id(execution_id: str) -> dict | None:
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    cur.execute(
        "SELECT * FROM executions WHERE execution_id = %s LIMIT 1;",
        (execution_id,)
    )
    row = cur.fetchone()

    cur.close()
    conn.close()

    return dict(row) if row else None


def get_previous_by_sequence(sequence_number: int) -> dict | None:
    if sequence_number <= 1:
        return None

    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    cur.execute(
        "SELECT * FROM executions WHERE sequence_number = %s LIMIT 1;",
        (sequence_number - 1,)
    )
    row = cur.fetchone()

    cur.close()
    conn.close()

    return dict(row) if row else None

from psycopg2.extras import RealDictCursor


def get_all_executions_ordered():
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    cur.execute("""
        SELECT *
        FROM executions
        ORDER BY sequence_number ASC;
    """)

    rows = cur.fetchall()

    cur.close()
    conn.close()

    return [dict(r) for r in rows]
