import sqlite3

conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

# Get all tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

print("Tables in database:")
for table in tables:
    print(f"  - {table[0]}")

# Check specifically for health_userprofile
if ('health_userprofile',) in tables:
    print("\n✓ health_userprofile table exists")
else:
    print("\n✗ health_userprofile table does NOT exist")

conn.close()
