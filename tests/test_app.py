import sys
import os
import pytest

# Add the project root folder to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_homepage(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"Welcome" in response.data  # Adjust if needed

def test_contact_page(client):
    response = client.get('/contact')
    assert response.status_code == 200
    assert b"Contact" in response.data  # Adjust if needed

def test_appointment_page(client):
    response = client.get('/appointment')
    assert response.status_code == 200
    assert b"Appointment" in response.data  # Adjust if needed

def test_blog_page(client):
    response = client.get('/blog')
    assert response.status_code == 200
    assert b"Blog" in response.data  # Adjust if needed

def test_successful_appointment(client):
    response = client.post(
        '/appointment',
        data={
            'name': 'Test User',
            'email': 'test@example.com',
            'date': '2025-06-22',
            'service': 'Consultation'
        },
        content_type='application/x-www-form-urlencoded',
        follow_redirects=True
    )
    assert response.status_code == 200
    assert b"Thank you for your message" in response.data or b"Success" in response.data

def test_appointment_missing_fields(client):
    response = client.post('/appointment', data={}, follow_redirects=True)
    assert response.status_code == 400  # Missing fields returns 400
