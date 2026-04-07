"""
LTCOE Campus — Flask Backend
Run: python app.py
Then open: http://localhost:5000
"""

import sqlite3
import os
from datetime import date
from flask import Flask, jsonify, request, send_from_directory, g

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH  = os.path.join(BASE_DIR, 'database.db')
SCHEMA   = os.path.join(BASE_DIR, 'schema.sql')

app = Flask(__name__, static_folder=BASE_DIR, static_url_path='')

# ──────────────────────────────────────────────────────────────
# DATABASE HELPERS
# ──────────────────────────────────────────────────────────────

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db

@app.teardown_appcontext
def close_db(e=None):
    db = g.pop('db', None)
    if db:
        db.close()

def init_db():
    """Create tables and seed data if DB doesn't exist."""
    if not os.path.exists(DB_PATH):
        with sqlite3.connect(DB_PATH) as conn:
            with open(SCHEMA, 'r') as f:
                conn.executescript(f.read())
        print("[OK] Database initialised with seed data.")
    else:
        print("[OK] Database found at:", DB_PATH)

def row_to_dict(row):
    return dict(row) if row else None

def rows_to_list(rows):
    return [dict(r) for r in rows]

# ──────────────────────────────────────────────────────────────
# SERVE FRONTEND
# ──────────────────────────────────────────────────────────────

@app.route('/')
def index():
    resp = send_from_directory(BASE_DIR, 'ltcoe.html')
    resp.headers['Content-Type'] = 'text/html; charset=utf-8'
    resp.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    resp.headers['Pragma'] = 'no-cache'
    resp.headers['Expires'] = '0'
    return resp

# ──────────────────────────────────────────────────────────────
# AUTH
# ──────────────────────────────────────────────────────────────

@app.route('/api/login', methods=['POST'])
def login():
    data  = request.get_json()
    email = (data.get('email') or '').strip()
    pwd   = data.get('password', '')
    db    = get_db()
    user  = db.execute(
        "SELECT * FROM users WHERE email=? AND password=?", (email, pwd)
    ).fetchone()
    if not user:
        return jsonify({'success': False, 'error': 'Invalid email or password'}), 401
    return jsonify({'success': True, 'user': row_to_dict(user)})

# ──────────────────────────────────────────────────────────────
# STUDENTS / APPLICATIONS
# ──────────────────────────────────────────────────────────────

@app.route('/api/students', methods=['GET'])
def get_students():
    db   = get_db()
    rows = db.execute("SELECT * FROM students ORDER BY id").fetchall()
    return jsonify(rows_to_list(rows))


@app.route('/api/students', methods=['POST'])
def add_student():
    data   = request.get_json()
    first  = (data.get('first') or '').strip()
    last   = (data.get('last')  or '').strip()
    email  = (data.get('email') or '').strip()
    branch = (data.get('branch') or 'CE').strip()

    if not first or not last or not email:
        return jsonify({'ok': False, 'error': 'first, last, email required'}), 400

    db = get_db()

    # Auto-generate roll number (e.g. CE001)
    count = db.execute(
        "SELECT COUNT(*) FROM students WHERE branch=?", (branch,)
    ).fetchone()[0]
    roll = f"{branch}{str(count + 1).zfill(3)}"

    applied = data.get('applied') or date.today().isoformat()

    db.execute("""
        INSERT INTO students
          (roll, first, last, email, phone, branch, year,
           gender, dob, address, school, score, status, applied)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,'Pending',?)
    """, (
        roll, first, last, email,
        data.get('phone', ''),
        branch,
        data.get('year', 'SE'),
        data.get('gender', 'Male'),
        data.get('dob', ''),
        data.get('address', ''),
        data.get('school', ''),
        data.get('score', ''),
        applied,
    ))
    db.commit()
    new_id = db.execute("SELECT last_insert_rowid()").fetchone()[0]
    student = row_to_dict(db.execute("SELECT * FROM students WHERE id=?", (new_id,)).fetchone())
    return jsonify({'ok': True, 'student': student}), 201


@app.route('/api/students/<int:sid>/status', methods=['POST'])
def update_student_status(sid):
    data = request.get_json()
    role = (data.get('role') or 'Student').lower()
    
    if role not in ('administrator', 'admin', 'faculty'):
        return jsonify({'ok': False, 'error': 'Unauthorized'}), 403
        
    status = data.get('status', 'Pending')
    if status not in ('Approved', 'Rejected', 'Pending'):
        return jsonify({'ok': False, 'error': 'Invalid status'}), 400
    db = get_db()
    db.execute("UPDATE students SET status=? WHERE id=?", (status, sid))
    db.commit()
    return jsonify({'ok': True})


@app.route('/api/students/<int:sid>', methods=['DELETE'])
def delete_student(sid):
    role = request.args.get('role') or 'Student'
    if role.lower() not in ('administrator', 'admin'):
        return jsonify({'ok': False, 'error': 'Unauthorized: Only Admin can delete'}), 403
        
    db = get_db()
    db.execute("DELETE FROM students WHERE id=?", (sid,))
    db.commit()
    return jsonify({'ok': True})

# ──────────────────────────────────────────────────────────────
# ATTENDANCE
# ──────────────────────────────────────────────────────────────

@app.route('/api/attendance', methods=['GET'])
def get_attendance():
    """
    Returns attendance grouped as:
      { "2025-07-14": { "1": "P", "3": "A", ... }, ... }
    """
    db   = get_db()
    rows = db.execute(
        "SELECT date, student_id, status FROM attendance_log ORDER BY date"
    ).fetchall()

    log = {}
    for r in rows:
        d   = r['date']
        sid = str(r['student_id'])
        if d not in log:
            log[d] = {}
        log[d][sid] = r['status']
    return jsonify(log)


@app.route('/api/attendance', methods=['POST'])
def save_attendance():
    data    = request.get_json()
    role    = (data.get('role') or 'Student').lower()
    
    if role not in ('administrator', 'admin', 'faculty'):
        return jsonify({'ok': False, 'error': 'Unauthorized: Only Faculty/Admin can save sessions'}), 403

    att_date = data.get('date') or date.today().isoformat()
    subject  = data.get('subject') or 'General Session'
    records  = data.get('records', {})

    if not records:
        return jsonify({'ok': False, 'error': 'No records provided'}), 400

    db = get_db()
    for sid_str, status in records.items():
        if status not in ('P', 'A'):
            continue
        db.execute("""
            INSERT INTO attendance_log (date, student_id, subject, status)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(date, student_id, subject)
            DO UPDATE SET status=excluded.status
        """, (att_date, int(sid_str), subject, status))
    db.commit()
    return jsonify({'ok': True, 'saved': len(records)})


@app.route('/api/attendance/summary', methods=['GET'])
def attendance_summary():
    """Per-student totals: { student_id: { present, total } }"""
    db   = get_db()
    rows = db.execute("""
        SELECT student_id,
               SUM(CASE WHEN status='P' THEN 1 ELSE 0 END) AS present,
               COUNT(*) AS total
        FROM   attendance_log
        GROUP  BY student_id
    """).fetchall()
    result = {}
    for r in rows:
        pct = (r['present'] / r['total'] * 100) if r['total'] > 0 else 0.0
        result[str(r['student_id'])] = {'present': r['present'], 'total': r['total'], 'percentage': pct}
    return jsonify(result)


@app.route('/api/students/<int:sid>/history', methods=['GET'])
def student_history(sid):
    db   = get_db()
    rows = db.execute("""
        SELECT date, subject, status 
        FROM   attendance_log 
        WHERE  student_id=? 
        ORDER  BY date DESC
    """, (sid,)).fetchall()
    return jsonify(rows_to_list(rows))


@app.route('/api/reports/branch-wise', methods=['GET'])
def branch_reports():
    db   = get_db()
    rows = db.execute("""
        SELECT s.branch,
               SUM(CASE WHEN a.status='P' THEN 1 ELSE 0 END) AS present,
               COUNT(a.status) AS total
        FROM   students s
        LEFT JOIN attendance_log a ON s.id = a.student_id
        WHERE  s.status='Approved'
        GROUP  BY s.branch
    """).fetchall()
    
    res = {}
    for r in rows:
        pct = 0.0
        if r['total'] > 0:
            pct = (r['present'] / r['total']) * 100
        res[r['branch']] = {'present': r['present'], 'total': r['total'], 'percentage': pct}
    return jsonify(res)


@app.route('/api/reports/defaulters', methods=['GET'])
def defaulters():
    db   = get_db()
    # Filter students with < 75% attendance among those who have at least 1 record
    rows = db.execute("""
        SELECT s.id, s.first, s.last, s.roll,
               SUM(CASE WHEN a.status='P' THEN 1 ELSE 0 END) AS present,
               COUNT(a.status) AS total
        FROM   students s
        JOIN   attendance_log a ON s.id = a.student_id
        WHERE  s.status='Approved'
        GROUP  BY s.id
        HAVING (CAST(SUM(CASE WHEN a.status='P' THEN 1 ELSE 0 END) AS FLOAT) / COUNT(a.status)) < 0.75
    """).fetchall()
    return jsonify(rows_to_list(rows))

# ──────────────────────────────────────────────────────────────
# MISC
# ──────────────────────────────────────────────────────────────

@app.route('/api/stats', methods=['GET'])
def stats():
    db      = get_db()
    total   = db.execute("SELECT COUNT(*) FROM students WHERE status='Approved'").fetchone()[0]
    pending = db.execute("SELECT COUNT(*) FROM students WHERE status='Pending'").fetchone()[0]
    today   = date.today().isoformat()
    present = db.execute("SELECT COUNT(*) FROM attendance_log WHERE date=? AND status='P'", (today,)).fetchone()[0]
    return jsonify({
        'total_students': total, 
        'pending_admissions': pending, 
        'present_today': present
    })

# ──────────────────────────────────────────────────────────────
# MAIN
# ──────────────────────────────────────────────────────────────

if __name__ == '__main__':
    with app.app_context():
        init_db()
    print("\n[LTCOE Campus] System ready at --> http://localhost:5000\n")
    app.run(debug=True, port=5000)
