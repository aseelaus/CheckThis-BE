"""Testing TaskDefinition"""
from flask import json

from checkthis.tests import test_util


# HELPER FUNCTIONS

def get_all(app):
    return app.test_client().get('/TaskDefinitions/')


def get_by_id(app, task_definition_id):
    return app.test_client().get('/TaskDefinitions/' + str(task_definition_id) + '/')


def post(app, title, checklist_definition_id, description):
    post_headers = {
        'Content-Type': 'application/json'
    }
    post_body = {
        "title": title,
        "checklist_definition_id": checklist_definition_id,
        "description": description
    }

    return app.test_client().post('/TaskDefinitions/', data=json.dumps(post_body), headers=post_headers)


def put(app, task_definition_id, title, checklist_definition_id, description):
    put_headers = {
        'Content-Type': 'application/json'
    }
    put_body = {
        "id": task_definition_id,
        "title": title,
        "checklist_definition_id": checklist_definition_id,
        "description": description
    }

    return app.test_client().put('/TaskDefinitions/' + str(task_definition_id) + '/', data=json.dumps(put_body),
                                 headers=put_headers)


def delete(app, task_definition_id):
    return app.test_client().delete('/TaskDefinitions/' + str(task_definition_id) + '/')


# TESTS START HERE


def test_task_definition_bp_hello():
    """Test the TaskDefinition Blueprint route"""
    app = test_util.setup()

    response = app.test_client().get('/TaskDefinitions/hello')

    assert response.status_code == 200
    assert response.data.decode('utf-8') == 'Hello from the other side!'

    test_util.teardown()


def test_crud():
    app = test_util.setup()
    ### TEST CREATE ###
    # ARRANGE
    title = 'test_task_definition_crud_title'
    cd_id = 1
    descr = 'test_task_definition_crud_descr'

    # ACT
    post_response = post(app=app,
                         title=title,
                         checklist_definition_id=cd_id,
                         description=descr
                         )

    # ASSERT
    post_response_json = post_response.json
    assert post_response.status_code == 200
    assert post_response_json["title"] == title
    assert post_response_json["checklist_definition_id"] == cd_id
    assert post_response_json["description"] == descr

    td_id = post_response_json["id"]

    ### TEST READ ###
    # by ID
    get_response = get_by_id(app, td_id)
    assert get_response.status_code == 200
    assert get_response.json["title"] == title
    assert get_response.json["description"] == descr
    assert get_response.json["checklist_definition_id"] == cd_id

    # get all
    get_response = get_all(app)
    assert get_response.status_code == 200

    task_definition = get_response.json[0]
    assert task_definition["title"] == title
    assert task_definition["description"] == descr
    assert task_definition["checklist_definition_id"] == cd_id

    ### TEST UPDATE ###
    # ARRANGE
    new_title = 'test_task_definition_put_title'
    new_cd_id = ''
    new_descr = 'test_task_definition_put_descr'

    # ACT
    put_response = put(app=app, task_definition_id=td_id, title=new_title, checklist_definition_id=new_cd_id,
                       description=new_descr)

    # ASSERT
    assert put_response.status_code == 200
    assert put_response.json["id"] == td_id
    assert put_response.json["title"] == new_title
    assert put_response.json["description"] == new_descr
    assert put_response.json["checklist_definition_id"] == new_cd_id

    ### TEST DELETE ###
    # ARRANGE

    # ACT
    delete_response = delete(app=app, task_definition_id=td_id)
    assert delete_response.status_code == 200
    assert delete_response.json is None

    # ASSERT
    get_response = get_by_id(app=app, task_definition_id=td_id)
    assert get_response.json == {}

    test_util.teardown()
