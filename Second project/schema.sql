DROP TABLE IF EXISTS Users;
CREATE TABLE Users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT NOT NULL,
  name TEXT NOT NULL,
  email TEXT NOT NULL,
  password TEXT NOT NULL
);

INSERT INTO Users (username, name, email, password) VALUES ("Ramon", "Ramon", "ramon@hyper.no", "123")
