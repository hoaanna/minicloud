import os
import json
from flask import Flask, jsonify, request, g
import pymysql
from pymysql.cursors import DictCursor

app = Flask(__name__)

# DB config via env
DB_HOST = os.getenv("DB_HOST", "relational-database-server")
DB_PORT = int(os.getenv("DB_PORT", 3306))
DB_USER = os.getenv("DB_USER", "root")
DB_PASS = os.getenv("DB_PASS", "root")
DB_NAME = os.getenv("DB_NAME", "mycloud")

STUDENTS_JSON = "students.json"


def get_db():
    if "db" not in g:
        g.db = pymysql.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASS,
            database=DB_NAME,
            cursorclass=DictCursor,
            autocommit=True,
            charset="utf8mb4",
        )
    return g.db


@app.teardown_appcontext
def close_db(exc):
    db = g.pop("db", None)
    if db is not None:
        db.close()


# Simple health endpoint
@app.get("/hello")
def hello():
    return jsonify(message="Hello from App Server!")


# Endpoint that reads local JSON file (static data)
@app.get("/student")
def students_from_file():
    try:
        with open(STUDENTS_JSON, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        return jsonify(error="students.json not found"), 500
    return jsonify(data)


# --------- Endpoints using MariaDB ---------
@app.get("/students_db")
def list_students_db():
    db = get_db()
    with db.cursor() as cur:
        cur.execute("SELECT * FROM students;")
        rows = cur.fetchall()
    return jsonify(rows)


@app.get("/students_db/<int:student_id>")
def get_student_db(student_id):
    db = get_db()
    with db.cursor() as cur:
        cur.execute("SELECT * FROM students WHERE id=%s;", (student_id,))
        row = cur.fetchone()
    if not row:
        return jsonify(error="Student not found"), 404
    return jsonify(row)


@app.post("/students_db")
def create_student_db():
    payload = request.get_json() or {}
    student_id = payload.get("student_id")
    fullname = payload.get("fullname")
    major = payload.get("major")
    gpa = payload.get("gpa")

    if not (student_id and fullname):
        return jsonify(error="student_id and fullname are required"), 400

    db = get_db()
    with db.cursor() as cur:
        cur.execute(
            "INSERT INTO students (student_id, fullname, major, gpa) VALUES (%s,%s,%s,%s);",
            (student_id, fullname, major, gpa),
        )
        new_id = cur.lastrowid
        cur.execute("SELECT * FROM students WHERE id=%s;", (new_id,))
        row = cur.fetchone()
    return jsonify(row), 201


@app.put("/students_db/<int:student_id>")
def update_student_db(student_id):
    payload = request.get_json() or {}
    fields = {}
    for k in ("student_id", "fullname", "major", "gpa"):
        if k in payload:
            fields[k] = payload[k]
    if not fields:
        return jsonify(error="No fields to update"), 400

    db = get_db()
    set_clause = ", ".join(f"{k}=%s" for k in fields.keys())
    params = list(fields.values()) + [student_id]
    with db.cursor() as cur:
        cur.execute(f"UPDATE students SET {set_clause} WHERE id=%s;", params)
        cur.execute("SELECT * FROM students WHERE id=%s;", (student_id,))
        row = cur.fetchone()
    if not row:
        return jsonify(error="Student not found"), 404
    return jsonify(row)


@app.delete("/students_db/<int:student_id>")
def delete_student_db(student_id):
    db = get_db()
    with db.cursor() as cur:
        cur.execute("SELECT * FROM students WHERE id=%s;", (student_id,))
        row = cur.fetchone()
        if not row:
            return jsonify(error="Student not found"), 404
        cur.execute("DELETE FROM students WHERE id=%s;", (student_id,))
    return jsonify(message="Deleted", id=student_id)


if __name__ == "__main__":
    # dev server
    app.run(host="0.0.0.0", port=8081)
