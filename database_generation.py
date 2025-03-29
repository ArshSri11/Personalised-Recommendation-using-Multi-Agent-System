import pandas as pd
import sqlite3

# Load CSV files, keeping only necessary columns
users_df = pd.read_csv("Dataset\\data\\ml-100k\\user.csv", usecols=["user_id", "age", "gender", "occupation"])
items_df = pd.read_csv("Dataset\\data\\ml-100k\\item.csv", usecols=["item_id", "title", "release_date", "genre"])
history_df = pd.read_csv("Dataset\\data\\ml-100k\\dev.csv", usecols=["user_id", "item_id", "rating", "timestamp"])

# Connect to SQLite database (or create one if not exists)
conn = sqlite3.connect("movies_database.db")
cursor = conn.cursor()

# Create Users table
cursor.execute("""
CREATE TABLE IF NOT EXISTS Users (
    user_id INTEGER PRIMARY KEY,
    age INTEGER,
    gender TEXT,
    occupation TEXT
);
""")

# Create Items table
cursor.execute("""
CREATE TABLE IF NOT EXISTS Items (
    item_id INTEGER PRIMARY KEY,
    title TEXT,
    release_date TEXT,
    genre TEXT
);
""")

# Create History table
cursor.execute("""
CREATE TABLE IF NOT EXISTS History (
    user_id INTEGER,
    item_id INTEGER,
    rating INTEGER,
    timestamp INTEGER,
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (item_id) REFERENCES Items(item_id)
);
""")

conn.commit()

# Save DataFrames to SQLite
users_df.to_sql("Users", conn, if_exists="replace", index=False)
items_df.to_sql("Items", conn, if_exists="replace", index=False)
history_df.to_sql("History", conn, if_exists="replace", index=False)

# Close connection
conn.close()