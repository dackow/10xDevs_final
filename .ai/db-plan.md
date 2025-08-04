# SQLite Database Schema & Migration Plan: AI Flashcard Generator

This document outlines the database schema for the AI Flashcard Generator project, designed for SQLite, and includes the strategy for managing schema changes using migrations.

## 1. Tables

### `users`
| Column Name     | Data Type | Constraints                               | Description                              |
|-----------------|-----------|-------------------------------------------|------------------------------------------|
| `id`            | `INTEGER` | `PRIMARY KEY AUTOINCREMENT`               | Unique identifier for the user.          |
| `username`      | `TEXT`    | `UNIQUE`, `NOT NULL`                      | User's unique username.                  |
| `password_hash` | `TEXT`    | `NOT NULL`                                | Hashed password (e.g., using Bcrypt).    |
| `created_at`    | `DATETIME`| `NOT NULL DEFAULT CURRENT_TIMESTAMP`      | Timestamp of user account creation.      |
| `updated_at`    | `DATETIME`| `NOT NULL DEFAULT CURRENT_TIMESTAMP`      | Timestamp of the last user data update.  |

### `flashcard_sets`
| Column Name  | Data Type | Constraints                                                              | Description                               |
|--------------|-----------|--------------------------------------------------------------------------|-------------------------------------------|
| `id`         | `INTEGER` | `PRIMARY KEY AUTOINCREMENT`                                              | Unique identifier for the flashcard set.  |
| `user_id`    | `INTEGER` | `NOT NULL`, `REFERENCES users(id) ON DELETE CASCADE`                     | References the user who owns the set.     |
| `name`       | `TEXT`    | `NOT NULL`                                                               | Name of the flashcard set.                |
| `created_at` | `DATETIME`| `NOT NULL DEFAULT CURRENT_TIMESTAMP`                                     | Timestamp of set creation.                |
| `updated_at` | `DATETIME`| `NOT NULL DEFAULT CURRENT_TIMESTAMP`                                     | Timestamp of the last set update.         |
|              |           | `UNIQUE (user_id, name)`                                                 | Ensures set names are unique per user.    |

### `flashcards`
| Column Name  | Data Type | Constraints                                                                | Description                               |
|--------------|-----------|----------------------------------------------------------------------------|-------------------------------------------|
| `id`         | `INTEGER` | `PRIMARY KEY AUTOINCREMENT`                                              | Unique identifier for the flashcard.      |
| `set_id`     | `INTEGER` | `NOT NULL`, `REFERENCES flashcard_sets(id) ON DELETE CASCADE`            | References the set this card belongs to.  |
| `question`   | `TEXT`    | `NOT NULL`                                                                 | The question side of the flashcard.       |
| `answer`     | `TEXT`    | `NOT NULL`                                                                 | The answer side of the flashcard.         |
| `created_at` | `DATETIME`| `NOT NULL DEFAULT CURRENT_TIMESTAMP`                                     | Timestamp of flashcard creation.          |
| `updated_at` | `DATETIME`| `NOT NULL DEFAULT CURRENT_TIMESTAMP`                                     | Timestamp of the last flashcard update.   |

## 2. Relationships

-   **`users` to `flashcard_sets`**: One-to-Many.
-   **`flashcard_sets` to `flashcards`**: One-to-Many.

## 3. Indexes

1.  **Unique Index on `users(username)`**
2.  **Unique Composite Index on `flashcard_sets(user_id, name)`**
3.  **Index on `flashcard_sets(user_id)`**: `CREATE INDEX ix_flashcard_sets_user_id ON flashcard_sets (user_id);`
4.  **Index on `flashcards(set_id)`**: `CREATE INDEX ix_flashcards_set_id ON flashcards (set_id);`

## 4. Database Migrations with Alembic

To manage changes to the database schema over time, we will use **Alembic**, a database migration tool for SQLAlchemy.

### Setup

1.  **Install Alembic**:
    ```sh
    pip install alembic
    ```

2.  **Initialize Alembic**:
    Run this command in the project root. It will create a `migrations` directory and an `alembic.ini` configuration file.
    ```sh
    alembic init migrations
    ```

3.  **Configure `alembic.ini`**:
    Point Alembic to the SQLite database.
    ```ini
    sqlalchemy.url = sqlite:///./flashcards.db
    ```

4.  **Configure `migrations/env.py`**:
    Connect Alembic to the SQLAlchemy models so it can auto-generate migrations.
    ```python
    # At the top of the file
    from app.models import Base # Adjust the import path as needed

    # Inside the run_migrations_online function
    target_metadata = Base.metadata
    ```

### Workflow

1.  **Generate a Migration**:
    Whenever you change your SQLAlchemy models (e.g., add a table or a column), generate a new migration script.
    ```sh
    alembic revision --autogenerate -m "Describe the change here"
    ```
    *Example: `alembic revision --autogenerate -m "Create initial tables"`*

2.  **Review the Migration Script**:
    Alembic will generate a Python file in `migrations/versions/`. Always review this file to ensure it accurately reflects the intended changes.

3.  **Apply the Migration**:
    Apply the changes to the database.
    ```sh
    alembic upgrade head
    ```

4.  **Downgrade a Migration** (if needed):
    You can revert the last migration.
    ```sh
    alembic downgrade -1
    ```

## 5. Design Notes

-   **Authorization**: All authorization logic will be handled in the application layer. SQLite does not support Row-Level Security.
-   **Timestamps**: The `updated_at` column requires application-level logic or a database trigger to be automatically updated on modification.
-   **Foreign Keys**: `PRAGMA foreign_keys = ON;` must be enabled in SQLite for foreign key constraints to be enforced.