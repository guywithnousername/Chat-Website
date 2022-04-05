CREATE TABLE IF NOT EXISTS Users (
	ID INTEGER PRIMARY KEY,
   	Username TEXT NOT NULL,
	Pass TEXT NOT NULL,
	Bio TEXT DEFAULT 'This user does not have a bio.',
	Random TEXT,
	UNIQUE(Username)
);
CREATE TABLE IF NOT EXISTS Messages (
	ID INTEGER PRIMARY KEY,
	RoomName TEXT NOT NULL,
	Username TEXT,
	MSG TEXT NOT NULL,
	Timestring TEXT,
	Time INTEGER,
	Anon INTEGER
);
CREATE TABLE IF NOT EXISTS Rooms (
	ID INTEGER PRIMARY KEY,
	RName TEXT NOT NULL,
	Pass TEXT NOT NULL,
	UNIQUE(RName)
);
CREATE TABLE IF NOT EXISTS Friends (
	ID INTEGER PRIMARY KEY,
	Friend1 TEXT NOT NULL,
	Friend2 TEXT NOT NULL,
	Code TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS UserMessages (
	ID INTEGER PRIMARY KEY,
	Recipient TEXT NOT NULL,
	MSG TEXT NOT NULL,
	Time INTEGER,
	Read INTEGER
);
CREATE TABLE IF NOT EXISTS Coins (
	ID INTEGER PRIMARY KEY,
	Username TEXT NOT NULL,
       	Num INTEGER,
	Box INTEGER	
);
CREATE TABLE IF NOT EXISTS Block (
	ID INTEGER PRIMARY KEY,
	Blocker TEXT NOT NULL,
	Blocked TEXT NOT NULL,
	ALLIP INTEGER
);
