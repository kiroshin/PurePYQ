/*
 * schema.sql
 * Created by Kiro Shin <mulgom@gmail.com> on 2024.
 */

CREATE TABLE IF NOT EXISTS human (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    username TEXT NOT NULL,
    gender TEXT NOT NULL,
    email TEXT NOT NULL,
    age INTEGER NOT NULL,
    country TEXT NOT NULL,
    cellphone TEXT,
    photo TEXT
);