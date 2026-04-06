from flask import (Flask, render_template, request, redirect)
import sqlite3

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

# Create tables
def init_db():
    conn = get_db()
    conn.execute('CREATE TABLE IF NOT EXISTS students (id INTEGER PRIMARY KEY, name TEXT, course TEXT)')
    conn.execute('CREATE TABLE IF NOT EXISTS teachers (id INTEGER PRIMARY KEY, name TEXT, subject TEXT)')
    conn.execute('CREATE TABLE IF NOT EXISTS courses (id INTEGER PRIMARY KEY, name TEXT, duration TEXT)')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template("index.html")

# Students
@app.route('/students', methods=['GET', 'POST'])
def students():
    conn = get_db()
    if request.method == 'POST':
        name = request.form['name']
        course = request.form['course']
        conn.execute("INSERT INTO students (name, course) VALUES (?, ?)", (name, course))
        conn.commit()
        return redirect('/students')

    students_data = conn.execute("SELECT * FROM students").fetchall()
    return render_template("students.html", students=students_data)

@app.route('/delete_student/<int:id>')
def delete_student(id):
    conn = get_db()
    conn.execute("DELETE FROM students WHERE id=?", (id,))
    conn.commit()
    return redirect('/students')

# Teachers
@app.route('/teachers', methods=['GET', 'POST'])
def teachers():
    conn = get_db()
    if request.method == 'POST':
        name = request.form['name']
        subject = request.form['subject']
        conn.execute("INSERT INTO teachers (name, subject) VALUES (?, ?)",(name, subject))
        conn.commit()
        return redirect('/teachers')

    teachers_data= conn.execute("SELECT * FROM teachers").fetchall()
    return render_template("teachers.html", teachers=teachers_data)

# Courses
@app.route('/courses', methods=['GET', 'POST'])
def courses():
    conn = get_db()
    if request.method == 'POST':
        name = request.form['name']
        duration = request.form['duration']
        conn.execute("INSERT INTO courses (name, duration) VALUES (?, ?)", (name, duration))
        conn.commit()
        return redirect('/courses')

    courses_list= conn.execute("SELECT * FROM courses").fetchall()
    return render_template("courses.html", courses=courses_list)

if __name__ == "__main__":
    init_db()
    app.run(debug=True)