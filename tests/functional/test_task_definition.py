'''Testing TaskDefinition'''
from api import app

def test_task_definition_bp():
    '''Test the TaskDefinition Blueprint route'''
    response = app.test_client().get('/TaskDefinitions/hello')

    assert response.status_code == 200
    assert response.data.decode('utf-8') == 'Hello from the other side!'
