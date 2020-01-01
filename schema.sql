DROP TABLE IF EXISTS pastes;

CREATE TABLE pastes (
    id INTEGER PRIMARY KEY, 
    body TEXT NOT NULL,
    private_paste BOOLEAN,
    user TEXT,
    FOREIGN KEY(user) REFERENCES users(user)
);

DROP TABLE IF EXISTS users; 

CREATE TABLE users (
    user TEXT, 
    pw TEXT, 
    email TEXT
);

INSERT INTO users VALUES ('admin', 'pbkdf2:sha256:150000$FVqgGVkr$0a8583ad1f5ac878135186b2f64c0add8db4b1cac30692baba2b962f05725083', 'admin@ad.ad'); 
INSERT INTO users VALUES ('ted', 'pbkdf2:sha256:150000$SmgSnG0U$fbe45c8bfc088537190f47a77004e50114eca132e75a7142f9eaffdfd4704fe2', 'ted@ted.ted');