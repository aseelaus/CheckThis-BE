"""Testing TaskDefinition"""
from flask import json

from checkthis.tests import test_util


def test_task_definition_bp_hello():
    """Test the TaskDefinition Blueprint route"""
    app = test_util.setup()

    response = app.test_client().get('/TaskDefinitions/hello')

    assert response.status_code == 200
    assert response.data.decode('utf-8') == 'Hello from the other side!'

    test_util.teardown()
# TODO implement api tests

def test_task_definition_get():
    app = test_util.setup()
    response = app.test_client().get('/TaskDefinitions/')

    assert response.status_code == 200
    test_util.teardown()


def test_task_definition_crud():
    app = test_util.setup()
    ### TEST CREATE ###
    # ARRANGE
    post_title = "Task Definition Created by pytest"
    post_cd_id = ""
    post_descr = "Task Definition Created by pytest"

    post_headers = {
        'Content-Type': 'application/json'
    }
    post_body = {
        "title": post_title,
        "checklist_definition_id": post_cd_id,
        "description": post_descr
    }

    # ACT
    post_response = app.test_client().post('/TaskDefinitions/', data=json.dumps(post_body), headers=post_headers)

    # ASSERT
    post_response_json = post_response.json
    assert post_response.status_code == 200
    assert post_response_json["title"] == post_title
    assert post_response_json["description"] == post_descr
    assert post_response_json["checklist_definition_id"] == post_cd_id

    td_id = post_response_json["id"]

    ### TEST READ ###
    get_response = app.test_client().get('/TaskDefinitions/'+str(td_id)+'/')
    assert get_response.status_code == 200
    assert get_response.json["title"] == post_title
    assert get_response.json["description"] == post_descr
    assert get_response.json["checklist_definition_id"] == post_cd_id
    test_util.teardown()
