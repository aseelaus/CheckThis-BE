"""Testing ChecklistDefinition"""
from flask import json

from checkthis.tests import test_util


# HELPER FUNCTIONS

def get_all(app):
    return app.test_client().get('/ChecklistDefinitions/')


def get_by_id(app, checklist_definition_id):
    return app.test_client().get('/ChecklistDefinitions/' + str(checklist_definition_id) + '/')


def post(app, title, description):
    post_headers = {
        'Content-Type': 'application/json'
    }
    post_body = {
        "title": title,
        "description": description
    }

    return app.test_client().post('/ChecklistDefinitions/', data=json.dumps(post_body), headers=post_headers)


def put(app, checklist_definition_id, title, description):
    put_headers = {
        'Content-Type': 'application/json'
    }
    put_body = {
        "id": checklist_definition_id,
        "title": title,
        "description": description
    }

    return app.test_client().put('/ChecklistDefinitions/' + str(checklist_definition_id) + '/', data=json.dumps(put_body),
                                 headers=put_headers)


def delete(app, task_definition_id):
    return app.test_client().delete('/ChecklistDefinitions/' + str(task_definition_id) + '/')


# TESTS START HERE


def test_checklist_definition_bp_hello():
    """Test the ChecklistDefinition Blueprint route"""
    app = test_util.setup()

    response = app.test_client().get('/ChecklistDefinitions/hello')

    assert response.status_code == 200
    assert response.data.decode('utf-8') == 'Hello from the other side!'

    test_util.teardown()


def test_crud():
    app = test_util.setup()
    ### TEST CREATE ###
    # ARRANGE
    title = 'test_checklist_definition_crud_title'
    descr = 'test_checklist_definition_crud_descr'

    # ACT
    post_response = post(app=app,
                         title=title,
                         description=descr
                         )

    # ASSERT
    post_response_json = post_response.json
    assert post_response.status_code == 200
    assert post_response_json["title"] == title
    assert post_response_json["description"] == descr

    cd_id = post_response_json["id"]

    ### TEST READ ###
    # by ID
    get_response = get_by_id(app, cd_id)
    assert get_response.status_code == 200
    assert get_response.json["title"] == title
    assert get_response.json["description"] == descr

    # get all
    get_response = get_all(app)
    assert get_response.status_code == 200

    checklist_definition = get_response.json[0]
    assert checklist_definition["title"] == title
    assert checklist_definition["description"] == descr

    ### TEST UPDATE ###
    # ARRANGE
    new_title = 'test_task_definition_put_title'
    new_descr = 'test_task_definition_put_descr'

    # ACT
    put_response = put(app=app, checklist_definition_id=cd_id, title=new_title, description=new_descr)

    # ASSERT
    assert put_response.status_code == 200
    assert put_response.json["id"] == cd_id
    assert put_response.json["title"] == new_title
    assert put_response.json["description"] == new_descr

    get_response = get_by_id(app, cd_id)
    assert get_response.status_code == 200
    assert get_response.json["title"] == new_title
    assert get_response.json["description"] == new_descr

    ### TEST DELETE ###
    # ARRANGE

    # ACT
    delete_response = delete(app=app, task_definition_id=cd_id)

    # ASSERT
    assert delete_response.status_code == 200
    assert delete_response.json is None

    get_response = get_by_id(app=app, checklist_definition_id=cd_id)
    assert get_response.status_code == 200
    assert get_response.json == {}

    test_util.teardown()
