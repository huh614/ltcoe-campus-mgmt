# LTCOE.int — Smart Campus Platform

Lokmanya Tilak College of Engineering's unified platform for **admissions**, **attendance tracking**, and **academic analytics** — backed by a real SQLite database.

---

## How to Run

### Prerequisites
- **Python 3** must be installed. Download from [python.org](https://www.python.org/downloads/)

### Step 1 — Install dependencies (one-time only)
Open a terminal / Command Prompt in this folder and run:

```
py -m pip install flask flask-cors
```

### Step 2 — Start the server

```
py app.py
```

You should see:
```
[OK] Database found at: ...
[LTCOE.int] Running at --> http://localhost:5000
 * Running on http://127.0.0.1:5000
```

### Step 3 — Open the app

Open your browser and go to:
```
http://localhost:5000
```

### Step 4 — Login

| Role          | Email                       | Password     |
|---------------|-----------------------------|--------------|
| Administrator | admin@ltcoe.edu.in          | admin123     |
| Faculty       | faculty@ltcoe.edu.in        | faculty123   |
| Student       | student@ltcoe.edu.in        | student123   |

---

## Project Structure

```
ltcoe-project/
├── app.py           ← Flask backend (REST API + file server)
├── schema.sql       ← SQLite schema + seed data (auto-runs first time)
├── database.db      ← SQLite database (auto-created on first run)
├── requirements.txt ← Python dependencies
├── ltcoe.html       ← Frontend (single-page app)
└── README.md        ← This file
```

---

## Features

| Module           | Description                                            |
|------------------|--------------------------------------------------------|
| **Dashboard**    | Live stats: students, attendance, trends, at-risk list |
| **Admissions**   | Add, approve, reject, delete applications              |
| **Students**     | Browse enrolled students, filter by branch             |
| **Attendance**   | Mark P/A per student per subject, save to DB           |
| **Records**      | Per-student attendance history with calendar view      |
| **Analytics**    | Branch-wise report, defaulters list, full summary      |
| **Alerts**       | Low attendance warnings, pending application alerts    |
| **Profile**      | Current user info, system stats                        |

---

## Database Tables

| Table              | Description                          |
|--------------------|--------------------------------------|
| `users`            | Login credentials and roles          |
| `students`         | All student/application records      |
| `attendance_log`   | Per-student, per-date, per-subject   |

---

## API Endpoints

| Method | URL                              | Description                  |
|--------|----------------------------------|------------------------------|
| POST   | `/api/login`                     | Authenticate user            |
| GET    | `/api/students`                  | List all students            |
| POST   | `/api/students`                  | Create new application       |
| PUT    | `/api/students/<id>/status`      | Approve / Reject / Pending   |
| DELETE | `/api/students/<id>`             | Delete student record        |
| GET    | `/api/attendance`                | All attendance logs          |
| POST   | `/api/attendance`                | Save a session               |
| GET    | `/api/attendance/summary`        | Per-student totals           |
| GET    | `/api/stats`                     | Quick stats for dashboard    |

---

## Notes

- Data **persists** between sessions — all changes are saved to `database.db`
- To **reset data**, delete `database.db` and restart the server (it re-seeds automatically)
- The server runs in **debug mode** — perfect for development/mini-project demo
- To stop the server: press `Ctrl + C` in the terminal
