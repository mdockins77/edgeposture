-- EdgePosture D1 Schema
-- Migration 0001

CREATE TABLE IF NOT EXISTS users (
  id TEXT PRIMARY KEY,
  email TEXT UNIQUE NOT NULL,
  name TEXT NOT NULL,
  password_hash TEXT NOT NULL,
  created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS scans (
  id TEXT PRIMARY KEY,
  url TEXT NOT NULL,
  final_url TEXT,
  user_id TEXT REFERENCES users(id),
  scanned_at TEXT NOT NULL,
  ttfb INTEGER,
  overall_score INTEGER,
  security_score INTEGER,
  performance_score INTEGER,
  compliance_score INTEGER,
  cdn_score INTEGER,
  summary TEXT,
  findings_json TEXT,
  recommendations_json TEXT
);

CREATE INDEX IF NOT EXISTS idx_scans_user ON scans(user_id);
CREATE INDEX IF NOT EXISTS idx_scans_url ON scans(url);
CREATE INDEX IF NOT EXISTS idx_scans_date ON scans(scanned_at DESC);
