import sqlite3

def view_appointments():
    conn = sqlite3.connect('appointments.db')
    cursor = conn.cursor()

    cursor.execute("SELECT name, email, date, service FROM appointments")
    rows = cursor.fetchall()

    if not rows:
        print("No appointments found.")
    else:
        for row in rows:
            name, email, date, service = row
            print(f"Name: {name}, Email: {email}, Date: {date}, Service: {service}")

    conn.close()

if __name__ == "__main__":
    view_appointments()
