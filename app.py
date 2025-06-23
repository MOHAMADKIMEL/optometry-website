from flask import Flask, render_template, request, redirect, url_for
import json
import os
import sqlite3

app = Flask(__name__)

# Initialize the appointments table if it doesn't exist
def init_db():
    conn = sqlite3.connect('appointments.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            date TEXT,
            service TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Load blog posts from JSON and add content from text files
def load_blog_posts():
    try:
        filepath = os.path.join('data', 'blog_posts.json')
        with open(filepath, 'r') as f:
            posts = json.load(f)
    except FileNotFoundError:
        return []

    for post in posts:
        content_path = os.path.join('blog_posts', f"{post['slug']}.txt")
        if os.path.exists(content_path):
            with open(content_path, 'r', encoding='utf-8') as content_file:
                post['content'] = content_file.read()
        else:
            post['content'] = "(Content not available.)"

    return posts

# Homepage
@app.route('/')
def home():
    return render_template('index.html')

# Services page
@app.route('/services')
def services():
    return render_template('services.html')

# Contact page with form - now stores in contacts table
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get("name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        message = request.form.get("message")

        conn = sqlite3.connect('appointments.db')
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS contacts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                email TEXT,
                phone TEXT,
                message TEXT
            )
        ''')
        c.execute("INSERT INTO contacts (name, email, phone, message) VALUES (?, ?, ?, ?)",
                  (name, email, phone, message))
        conn.commit()
        conn.close()

        return render_template("success.html", message="Thank you for your message! We will contact you soon.")
    return render_template("contact.html")

# Appointment booking page
@app.route('/appointment', methods=['GET', 'POST'])
def appointment():
    if request.method == 'POST':
        name = request.form.get("name")
        email = request.form.get("email")
        date = request.form.get("date")
        service = request.form.get("service")

        if not all([name, email, date, service]):
            return "Missing fields in the form", 400

        conn = sqlite3.connect('appointments.db')
        c = conn.cursor()
        # Table is created in init_db() so no need here but okay to keep for safety
        c.execute('''
            CREATE TABLE IF NOT EXISTS appointments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                email TEXT,
                date TEXT,
                service TEXT
            )
        ''')
        c.execute("INSERT INTO appointments (name, email, date, service) VALUES (?, ?, ?, ?)", 
                  (name, email, date, service))
        conn.commit()
        conn.close()

        return render_template("success.html", message="Thank you for your appointment! We will contact you soon to confirm the details.")
    return render_template('appointment.html')

# Success message page
@app.route('/success')
def success():
    return render_template('success.html')

# Blog page that loads blog posts
@app.route('/blog')
def blog():
    posts = load_blog_posts()
    return render_template('blog.html', posts=posts)

# Individual blog post page
@app.route('/blog/<slug>')
def blog_post(slug):
    posts = load_blog_posts()
    for post in posts:
        if post['slug'] == slug:
            return render_template('blog_post.html', post=post)
    return "Post not found", 404

# Symptom Checker page
@app.route('/symptom-checker')
def symptom_checker():
    return render_template('symptom_checker.html')

# View appointments page
@app.route('/view-appointments')
def view_appointments():
    conn = sqlite3.connect('appointments.db')
    c = conn.cursor()
    c.execute("SELECT id, name, email, date, service FROM appointments")
    appointments = c.fetchall()
    conn.close()
    return render_template('view_appointments.html', appointments=appointments)

# View contacts page
@app.route('/view-contacts')
def view_contacts():
    conn = sqlite3.connect('appointments.db')
    c = conn.cursor()
    c.execute("SELECT id, name, email, phone, message FROM contacts")
    contacts = c.fetchall()
    conn.close()
    return render_template('view_contacts.html', contacts=contacts)

if __name__ == '__main__':
    init_db()  # Make sure appointments table exists before app runs
    app.run(debug=True)
