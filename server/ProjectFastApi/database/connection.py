import aiosqlite
import os
from pathlib import Path

DATABASE_PATH = "service.db"


async def get_db():
    async with aiosqlite.connect(DATABASE_PATH) as db:
        db.row_factory = aiosqlite.Row
        yield db


async def init_db():
    """Initialize database tables"""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        # Users table
        await db.execute("""
                         CREATE TABLE IF NOT EXISTS users
                         (
                             id
                             INTEGER
                             PRIMARY
                             KEY
                             AUTOINCREMENT,
                             email
                             TEXT
                             UNIQUE
                             NOT
                             NULL,
                             password
                             TEXT
                             NOT
                             NULL,
                             firstname
                             TEXT
                             NOT
                             NULL,
                             lastname
                             TEXT
                             NOT
                             NULL,
                             role
                             TEXT
                             DEFAULT
                             'user',
                             created_at
                             TIMESTAMP
                             DEFAULT
                             CURRENT_TIMESTAMP
                         )
                         """)

        # Services table
        await db.execute("""
                         CREATE TABLE IF NOT EXISTS services
                         (
                             id
                             INTEGER
                             PRIMARY
                             KEY
                             AUTOINCREMENT,
                             device_model
                             TEXT
                             NOT
                             NULL,
                             issue_type
                             TEXT
                             NOT
                             NULL,
                             problem_area
                             TEXT
                             NOT
                             NULL,
                             description
                             TEXT
                             NOT
                             NULL,
                             location
                             TEXT
                             NOT
                             NULL,
                             owner_id
                             INTEGER
                             NOT
                             NULL,
                             master_id
                             INTEGER,
                             price
                             REAL,
                             finished_at
                             TIMESTAMP,
                             status
                             TEXT
                             DEFAULT
                             'pending',
                             created_at
                             TIMESTAMP
                             DEFAULT
                             CURRENT_TIMESTAMP,
                             updated_at
                             TIMESTAMP
                             DEFAULT
                             CURRENT_TIMESTAMP,
                             FOREIGN
                             KEY
                         (
                             owner_id
                         ) REFERENCES users
                         (
                             id
                         ),
                             FOREIGN KEY
                         (
                             master_id
                         ) REFERENCES users
                         (
                             id
                         )
                             )
                         """)

        # Components table
        await db.execute("""
                         CREATE TABLE IF NOT EXISTS components
                         (
                             id
                             INTEGER
                             PRIMARY
                             KEY
                             AUTOINCREMENT,
                             name
                             TEXT
                             NOT
                             NULL,
                             description
                             TEXT
                             NOT
                             NULL,
                             price
                             REAL
                             NOT
                             NULL,
                             quantity
                             INTEGER
                             NOT
                             NULL,
                             created_at
                             TIMESTAMP
                             DEFAULT
                             CURRENT_TIMESTAMP
                         )
                         """)

        # Service components (many-to-many relationship)
        await db.execute("""
                         CREATE TABLE IF NOT EXISTS service_components
                         (
                             id
                             INTEGER
                             PRIMARY
                             KEY
                             AUTOINCREMENT,
                             service_id
                             INTEGER
                             NOT
                             NULL,
                             component_id
                             INTEGER
                             NOT
                             NULL,
                             quantity
                             INTEGER
                             NOT
                             NULL,
                             FOREIGN
                             KEY
                         (
                             service_id
                         ) REFERENCES services
                         (
                             id
                         ),
                             FOREIGN KEY
                         (
                             component_id
                         ) REFERENCES components
                         (
                             id
                         )
                             )
                         """)

        await db.commit()
        print("Database initialized successfully")
