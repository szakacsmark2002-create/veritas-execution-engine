import psycopg2
from psycopg2.extras import Json
from uuid import uuid4
from datetime import datetime


DB_NAME = "saco_db"
DB_USER = "postgres"
DB_HOST = "localhost"
DB_PORT = 5432


def get_connection():
    return psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        host=DB_HOST,
        port=DB_PORT
    )


def insert_execution(record: dict):

    conn = get_connection()
    cur = conn.cursor()

    execution_id = uuid4()
    ts_utc = datetime.utcnow()

    cur.execute("""
        INSERT INTO executions (
            execution_id,
            ts_utc,
            engine_version,
            schema_version,
            input_hash,
            world_hash,
            result_hash,
            execution_hash,
            input_json,
            world_json,
            result_json
        )
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """, (
        execution_id,
        ts_utc,
        record["engine_version"],
        record["schema_version"],
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

    return str(execution_id)
