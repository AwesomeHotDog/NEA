import sqlite3

# Connect to the database
conn = sqlite3.connect("cinema_system.db")
cursor = conn.cursor()

# Sample movies
movies = [
    ("Inception", "Sci-Fi", 148, "2010-07-16"),
    ("The Dark Knight", "Action", 152, "2008-07-18"),
    ("Interstellar", "Sci-Fi", 169, "2014-11-07"),
    ("Titanic", "Romance", 195, "1997-12-19"),
    ("Avengers: Endgame", "Action", 181, "2019-04-26"),
    ("Joker", "Drama", 122, "2019-10-04"),
    ("The Matrix", "Sci-Fi", 136, "1999-03-31"),
    ("The Godfather", "Crime", 175, "1972-03-24"),
    ("The Shawshank Redemption", "Drama", 142, "1994-09-23"),
    ("Pulp Fiction", "Crime", 154, "1994-10-14"),
    ("Forrest Gump", "Drama", 142, "1994-07-06"),
    ("Gladiator", "Action", 155, "2000-05-05"),
]

# Insert movies into the Movies table
try:
    cursor.executemany("INSERT INTO Movies (title, genre, duration, release_date) VALUES (?, ?, ?, ?)", movies)
    conn.commit()
    print("✅ Movies have been successfully added to the database!")
except sqlite3.Error as e:
    print(f"❌ Error inserting movies: {e}")
finally:
    conn.close()
