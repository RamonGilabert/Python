CREATE TABLE IF NOT EXISTS Users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL UNIQUE,
  nfc TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS Users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  temperature FLOAT NOT NULL UNIQUE,
  created DATE NOT NULL,
  difference FLOAT NOT NULL
);
