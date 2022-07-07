"""Testing TaskDefinition"""
from run import app


def test_task_definition_bp_hello():
    """Test the TaskDefinition Blueprint route"""
    response = app.test_client().get('/TaskDefinitions/hello')

    assert response.status_code == 200
    assert response.data.decode('utf-8') == 'Hello from the other side!'

# TODO implement api tests

def test_task_definition_get():
    response = app.test_client().get('/TaskDefinitions/')

    assert response.status_code == 200
