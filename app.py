from flask import Flask, render_template, request, redirect, url_for
import json
import os
import sqlite3

app = Flask(__name__)

# Database initialization

def init_db():
    """
    Create the appointments database with a table if it doesn't exist.
    Also ensures the app can store contact messages.
    """
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


def load_blog_posts():
    """
    Load blog metadata from a JSON file and actual blog content
    from corresponding .txt files in /blog_posts directory.
    """
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


@app.route('/')
def home():
    """Render homepage"""
    return render_template('index.html')

@app.route('/services')
def services():
    """Render services page"""
    return render_template('services.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    """
    Handle contact form submission and save to database.
    Displays thank-you message after successful submission.
    """
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

@app.route('/appointment', methods=['GET', 'POST'])
def appointment():
    """
    Handle appointment booking form and save data to the appointments table.
    Shows success message after submission.
    """
    if request.method == 'POST':
        name = request.form.get("name")
        email = request.form.get("email")
        date = request.form.get("date")
        service = request.form.get("service")

        if not all([name, email, date, service]):
            return "Missing fields in the form", 400

        conn = sqlite3.connect('appointments.db')
        c = conn.cursor()
        
        # Make sure the appointments table exists
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

@app.route('/success')
def success():
    """Generic success page for form submissions"""
    return render_template('success.html')

@app.route('/blog')
def blog():
    """List all blog posts using data from JSON and text files"""
    posts = load_blog_posts()
    return render_template('blog.html', posts=posts)

@app.route('/blog/<slug>')
def blog_post(slug):
    """Render a single blog post by slug (filename)"""
    posts = load_blog_posts()
    for post in posts:
        if post['slug'] == slug:
            return render_template('blog_post.html', post=post)
    return "Post not found", 404

@app.route('/symptom-checker')
def symptom_checker():
    """Placeholder page for a future symptom checker tool"""
    return render_template('symptom_checker.html')

@app.route('/view-appointments')
def view_appointments():
    """Admin page to view all appointments stored in the database"""
    conn = sqlite3.connect('appointments.db')
    c = conn.cursor()
    c.execute("SELECT id, name, email, date, service FROM appointments")
    appointments = c.fetchall()
    conn.close()
    return render_template('view_appointments.html', appointments=appointments)

@app.route('/view-contacts')
def view_contacts():
    """Admin page to view all contact form submissions"""
    conn = sqlite3.connect('appointments.db')
    c = conn.cursor()
    c.execute("SELECT id, name, email, phone, message FROM contacts")
    contacts = c.fetchall()
    conn.close()
    return render_template('view_contacts.html', contacts=contacts)

if __name__ == '__main__':
    init_db()  
    app.run(debug=True)  