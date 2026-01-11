from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
DB_PATH = "movies.db"


def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/", methods=["GET", "POST"])
def home():
    conn = get_db_connection()

    if request.method == "POST":
        ids = request.form.getlist("movieToRemove")
        for movie_id in ids:
            conn.execute("DELETE FROM movies WHERE id = ?", (movie_id,))
        conn.commit()

    movies = conn.execute(
        "SELECT id, title, year, actors FROM movies"
    ).fetchall()

    conn.close()
    return render_template("home.html", movies=movies)


@app.route("/addMovie", methods=["GET", "POST"])
def add_movie():
    if request.method == "POST":
        title = request.form.get("title")
        year = request.form.get("year")
        actors = request.form.get("actors")

        conn = get_db_connection()
        conn.execute(
            "INSERT INTO movies (title, year, actors) VALUES (?, ?, ?)",
            (title, year, actors)
        )
        conn.commit()
        conn.close()

        return redirect(url_for("home"))

    return render_template("add.html")


if __name__ == "__main__":
    app.run(debug=True)
