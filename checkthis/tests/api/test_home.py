"""Testing Home page"""
from checkthis import app


def test_home():
    """Test the return of the Home page"""
    response = app.test_client().get('/')

    assert response.status_code == 200
    assert response.data.decode('utf-8') == 'Feels like home!'
