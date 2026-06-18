DROP TABLE IF EXISTS files;

CREATE TABLE files (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    filename TEXT NOT NULL,

    path TEXT UNIQUE NOT NULL,

    extension TEXT,

    size INTEGER,

    content TEXT,

    line_count INTEGER,

    last_modified REAL,

    indexed_at DATETIME DEFAULT CURRENT_TIMESTAMP
);