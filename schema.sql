-- ============================================================
-- LTCOE Campus — SQLite Schema
-- ============================================================

PRAGMA foreign_keys = ON;

-- ── Users (login) ───────────────────────────────────────────
CREATE TABLE IF NOT EXISTS users (
  id        INTEGER PRIMARY KEY AUTOINCREMENT,
  email     TEXT    UNIQUE NOT NULL,
  password  TEXT    NOT NULL,
  role      TEXT    NOT NULL,   -- 'Administrator' | 'Faculty' | 'Student'
  name      TEXT    NOT NULL,
  initials  TEXT    NOT NULL
);

-- ── Students / Applications ─────────────────────────────────
CREATE TABLE IF NOT EXISTS students (
  id        INTEGER PRIMARY KEY AUTOINCREMENT,
  roll      TEXT,
  first     TEXT    NOT NULL,
  last      TEXT    NOT NULL,
  email     TEXT    NOT NULL,
  phone     TEXT,
  branch    TEXT    NOT NULL,   -- CE | IT | ENTC | Mech | Civil
  year      TEXT    NOT NULL,   -- FE | SE | TE | BE
  gender    TEXT,
  dob       TEXT,
  address   TEXT,
  school    TEXT,
  score     TEXT,
  status    TEXT    NOT NULL DEFAULT 'Pending',  -- Pending | Approved | Rejected
  applied   TEXT    NOT NULL
);

-- ── Attendance Log ───────────────────────────────────────────
CREATE TABLE IF NOT EXISTS attendance_log (
  id         INTEGER PRIMARY KEY AUTOINCREMENT,
  date       TEXT    NOT NULL,
  student_id INTEGER NOT NULL REFERENCES students(id) ON DELETE CASCADE,
  subject    TEXT    NOT NULL DEFAULT 'General Session',
  status     TEXT    NOT NULL,  -- 'P' | 'A'
  UNIQUE(date, student_id, subject)
);

-- ============================================================
-- SEED DATA
-- ============================================================

INSERT OR IGNORE INTO users (email, password, role, name, initials) VALUES
  ('admin@ltcoe.edu.in',   'admin123',   'Administrator', 'Prof. M. Umale',  'MU'),
  ('faculty@ltcoe.edu.in', 'faculty123', 'Faculty',       'Prof. A. Sharma', 'AS'),
  ('student@ltcoe.edu.in', 'student123', 'Student',       'Vedant Pawar',    'VP');

INSERT OR IGNORE INTO students (roll, first, last, email, phone, branch, year, gender, dob, address, school, score, status, applied) VALUES
  ('CE001',   'Vedant',  'Pawar',    'vedant@ltcoe.edu.in',  '9876543210', 'CE',   'SE', 'Male',   '2004-03-15', 'Pune, Maharashtra',       'Fergusson College Jr.',  '88.4%', 'Approved', '2025-07-01'),
  ('CE002',   'Purva',   'Pankar',   'purva@ltcoe.edu.in',   '9876543211', 'CE',   'SE', 'Female', '2004-05-20', 'Nagpur, Maharashtra',     'Hislop College Jr.',     '91.2%', 'Approved', '2025-07-01'),
  ('CE003',   'Shruti',  'Waykole',  'shruti@ltcoe.edu.in',  '9876543212', 'CE',   'SE', 'Female', '2004-08-11', 'Nashik, Maharashtra',     'Nashik Public Jr.',      '85.0%', 'Approved', '2025-07-02'),
  ('CE004',   'Swayam',  'Telang',   'swayam@ltcoe.edu.in',  '9876543213', 'CE',   'SE', 'Male',   '2004-01-30', 'Mumbai, Maharashtra',     'Elphinstone Jr.',        '87.8%', 'Approved', '2025-07-03'),
  ('IT001',   'Aditya',  'Sharma',   'aditya@ltcoe.edu.in',  '9876543214', 'IT',   'SE', 'Male',   '2004-06-22', 'Pune, Maharashtra',       'Nowrosjee Wadia Jr.',    '82.6%', 'Approved', '2025-07-05'),
  ('IT002',   'Sneha',   'More',     'sneha@ltcoe.edu.in',   '9876543215', 'IT',   'TE', 'Female', '2003-09-14', 'Aurangabad, Maharashtra', 'BAMU Jr.',               '79.4%', 'Approved', '2025-07-06'),
  ('CE005',   'Rahul',   'Desai',    'rahul@ltcoe.edu.in',   '9876543216', 'CE',   'TE', 'Male',   '2003-11-05', 'Solapur, Maharashtra',    'DAV Public Jr.',         '76.2%', 'Pending',  '2025-07-10'),
  ('CE006',   'Priya',   'Kulkarni', 'priya@ltcoe.edu.in',   '9876543217', 'CE',   'BE', 'Female', '2002-02-18', 'Kolhapur, Maharashtra',   'Shivaji Univ Jr.',       '93.1%', 'Pending',  '2025-07-12'),
  ('ENTC001', 'Rohan',   'Joshi',    'rohan@ltcoe.edu.in',   '9876543218', 'ENTC', 'SE', 'Male',   '2004-04-07', 'Pune, Maharashtra',       'MIT Jr.',                '74.0%', 'Rejected', '2025-07-08'),
  ('Mech001', 'Amit',    'Patil',    'amit@ltcoe.edu.in',    '9876543219', 'Mech', 'SE', 'Male',   '2004-07-19', 'Satara, Maharashtra',     'Satara Jr.',             '80.5%', 'Approved', '2025-07-14'),
  ('CE007',   'Kavya',   'Nair',     'kavya@ltcoe.edu.in',   '9876543220', 'CE',   'FE', 'Female', '2005-12-03', 'Thane, Maharashtra',      'Thane Jr.',              '95.2%', 'Pending',  '2025-07-15');

-- Seed attendance for approved students (ids 1-6, 10) across 7 days
-- Using fixed values for reproducibility
INSERT OR IGNORE INTO attendance_log (date, student_id, subject, status) VALUES
  ('2025-07-14', 1, 'General Session', 'P'), ('2025-07-14', 2, 'General Session', 'P'),
  ('2025-07-14', 3, 'General Session', 'A'), ('2025-07-14', 4, 'General Session', 'P'),
  ('2025-07-14', 5, 'General Session', 'A'), ('2025-07-14', 6, 'General Session', 'P'),
  ('2025-07-14', 10,'General Session', 'P'),

  ('2025-07-15', 1, 'General Session', 'P'), ('2025-07-15', 2, 'General Session', 'A'),
  ('2025-07-15', 3, 'General Session', 'P'), ('2025-07-15', 4, 'General Session', 'P'),
  ('2025-07-15', 5, 'General Session', 'A'), ('2025-07-15', 6, 'General Session', 'P'),
  ('2025-07-15', 10,'General Session', 'P'),

  ('2025-07-16', 1, 'General Session', 'P'), ('2025-07-16', 2, 'General Session', 'P'),
  ('2025-07-16', 3, 'General Session', 'P'), ('2025-07-16', 4, 'General Session', 'A'),
  ('2025-07-16', 5, 'General Session', 'P'), ('2025-07-16', 6, 'General Session', 'A'),
  ('2025-07-16', 10,'General Session', 'P'),

  ('2025-07-17', 1, 'General Session', 'P'), ('2025-07-17', 2, 'General Session', 'P'),
  ('2025-07-17', 3, 'General Session', 'A'), ('2025-07-17', 4, 'General Session', 'P'),
  ('2025-07-17', 5, 'General Session', 'A'), ('2025-07-17', 6, 'General Session', 'P'),
  ('2025-07-17', 10,'General Session', 'A'),

  ('2025-07-18', 1, 'General Session', 'P'), ('2025-07-18', 2, 'General Session', 'P'),
  ('2025-07-18', 3, 'General Session', 'P'), ('2025-07-18', 4, 'General Session', 'P'),
  ('2025-07-18', 5, 'General Session', 'A'), ('2025-07-18', 6, 'General Session', 'A'),
  ('2025-07-18', 10,'General Session', 'P'),

  ('2025-07-21', 1, 'General Session', 'A'), ('2025-07-21', 2, 'General Session', 'P'),
  ('2025-07-21', 3, 'General Session', 'P'), ('2025-07-21', 4, 'General Session', 'P'),
  ('2025-07-21', 5, 'General Session', 'A'), ('2025-07-21', 6, 'General Session', 'P'),
  ('2025-07-21', 10,'General Session', 'P'),

  ('2025-07-22', 1, 'General Session', 'P'), ('2025-07-22', 2, 'General Session', 'P'),
  ('2025-07-22', 3, 'General Session', 'P'), ('2025-07-22', 4, 'General Session', 'A'),
  ('2025-07-22', 5, 'General Session', 'A'), ('2025-07-22', 6, 'General Session', 'P'),
  ('2025-07-22', 10,'General Session', 'P');
