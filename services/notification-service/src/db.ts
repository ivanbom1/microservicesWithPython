import Database from "better-sqlite3";
import path from "path";

const db = new Database(path.join(__dirname, "notifications.db"));

db.exec(`
  CREATE TABLE IF NOT EXISTS notifications (
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id   TEXT    NOT NULL,
    message   TEXT    NOT NULL,
    received_at TEXT  NOT NULL DEFAULT (datetime('now'))
  )
`);

export default db;  
