import sqlite3

conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

# Create the health_userprofile table
cursor.execute('''
CREATE TABLE IF NOT EXISTS health_userprofile (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    profile_image VARCHAR(100),
    icon_image VARCHAR(100),
    bio VARCHAR(500),
    phone VARCHAR(20),
    date_of_birth DATE,
    address VARCHAR(255),
    created_at DATETIME,
    updated_at DATETIME,
    user_id INTEGER NOT NULL UNIQUE,
    FOREIGN KEY (user_id) REFERENCES auth_user (id)
);
''')

conn.commit()

# Verify it was created
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='health_userprofile';")
result = cursor.fetchone()

if result:
    print("✓ health_userprofile table created successfully")
else:
    print("✗ Failed to create health_userprofile table")

conn.close()
