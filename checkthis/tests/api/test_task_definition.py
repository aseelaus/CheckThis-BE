"""Testing TaskDefinition"""
from flask import json

from checkthis.tests import test_util
from checkthis.tests.api import test_checklist_definition


# HELPER FUNCTIONS


def get_all(app):
    return app.test_client().get('/TaskDefinitions/')


def get_by_id(app, task_definition_id):
    return app.test_client().get('/TaskDefinitions/' + str(task_definition_id) + '/')


def post(app, title, checklist_definition_id, parent_task_definition_id, description):
    post_headers = {
        'Content-Type': 'application/json'
    }
    post_body = {
        "title": title,
        "checklist_definition_id": checklist_definition_id,
        "parent_task_definition_id": parent_task_definition_id,
        "description": description
    }

    return app.test_client().post('/TaskDefinitions/',
                                  data=json.dumps(post_body),
                                  headers=post_headers)


def put(app, task_definition_id, title, description, checklist_definition_id=None, parent_task_definition_id=None):
    put_headers = {
        'Content-Type': 'application/json'
    }
    put_body = {
        "id": task_definition_id,
        "title": title,
        "checklist_definition_id": checklist_definition_id,
        "parent_task_definition_id": parent_task_definition_id,
        "description": description
    }

    return app.test_client().put('/TaskDefinitions/' + str(task_definition_id) + '/',
                                 data=json.dumps(put_body),
                                 headers=put_headers)


def delete(app, task_definition_id):
    return app.test_client().delete('/TaskDefinitions/' + str(task_definition_id) + '/')


# TESTS START HERE


def test_crud():
    app = test_util.setup()
    ### TEST CREATE ###
    # ARRANGE
    # create checklist definition to be referenced
    cd_post_response = test_checklist_definition.post(app, 'cd_title', 'cd_descr')
    cd_id = cd_post_response.json['id']

    title = 'test_task_definition_crud_title'
    descr = 'test_task_definition_crud_descr'

    # ACT
    post_response = post(app=app,
                         title=title,
                         checklist_definition_id=cd_id,
                         parent_task_definition_id=None,
                         description=descr
                         )

    # ASSERT
    post_response_json = post_response.json
    assert post_response.status_code == 200
    assert post_response_json["title"] == title
    assert post_response_json["checklist_definition_id"] == cd_id
    assert post_response_json["parent_task_definition_id"] is None
    assert post_response_json["description"] == descr

    td_id = post_response_json["id"]

    ### TEST READ ###
    # by ID
    get_response = get_by_id(app, td_id)
    assert get_response.status_code == 200
    assert get_response.json["title"] == title
    assert get_response.json["description"] == descr
    assert get_response.json["checklist_definition_id"] == cd_id
    assert get_response.json["parent_task_definition_id"] is None

    # get all
    get_response = get_all(app)
    assert get_response.status_code == 200

    task_definition = get_response.json[0]
    assert task_definition["title"] == title
    assert task_definition["description"] == descr
    assert task_definition["checklist_definition_id"] == cd_id
    assert task_definition["parent_task_definition_id"] is None

    ### TEST UPDATE ###
    # ARRANGE
    new_title = 'test_task_definition_put_title'
    new_descr = 'test_task_definition_put_descr'

    # ACT
    put_response = put(app=app,
                       task_definition_id=td_id,
                       title=new_title,
                       checklist_definition_id=cd_id,
                       description=new_descr,
                       parent_task_definition_id=None)

    # ASSERT
    assert put_response.status_code == 200
    assert put_response.json["id"] == td_id
    assert put_response.json["title"] == new_title
    assert put_response.json["description"] == new_descr
    assert put_response.json["checklist_definition_id"] == cd_id
    assert put_response.json["parent_task_definition_id"] is None

    ### TEST DELETE ###
    # ARRANGE

    # ACT
    delete_response = delete(app=app, task_definition_id=td_id)
    assert delete_response.status_code == 200
    assert delete_response.json is None

    # ASSERT
    get_response = get_by_id(app=app, task_definition_id=td_id)
    assert get_response.status_code == 404
    assert get_response.json is None

    test_util.teardown()


def test_object_not_found_rsp():
    app = test_util.setup()

    ### get by id ###
    # ARRANGE
    nonexistent_id = 500

    # ACT
    get_response = get_by_id(app=app,
                             task_definition_id=nonexistent_id)

    # ASSERT
    assert get_response.status_code == 404

    ### put ###
    # ARRANGE
    # ACT
    put_response = put(app=app,
                       task_definition_id=nonexistent_id,
                       title='some_title',
                       checklist_definition_id=123,
                       description='some_descr')

    # ASSERT
    assert put_response.status_code == 404

    ### delete ###
    # ARRANGE
    # ACT
    delete_response = delete(app=app,
                             task_definition_id=nonexistent_id)

    # ASSERT
    assert delete_response.status_code == 404

    test_util.teardown()


def test_db_integrity_error_rsp():
    app = test_util.setup()

    ### post ###
    # ARRANGE
    nonexistent_id = 500
    integrity_err_text = b"Database Integrity Error. Do all referenced objects exist?"
    # ACT
    post_response = post(app=app,
                         title='some title',
                         checklist_definition_id=nonexistent_id,
                         parent_task_definition_id=None,
                         description='some descr')
    # ASSERT
    assert post_response.status_code == 400
    assert post_response.data == integrity_err_text

    ### put ###
    # ARRANGE
    # create task definition (requires checklist definition)
    cd_post_response = test_checklist_definition.post(app=app,
                                                      title='cd_title',
                                                      description='cd_descr')
    cd_id = cd_post_response.json['id']

    td_post_response = post(app=app,
                            title='some title',
                            checklist_definition_id=cd_id,
                            parent_task_definition_id=None,
                            description='some descr')

    td_id = td_post_response.json['id']

    # ACT
    # try to change the checklist_definition_id to a nonexistent value, provoking a db integrity error
    put_response = put(app=app,
                       task_definition_id=td_id,
                       title='some title',
                       checklist_definition_id=nonexistent_id,
                       description='some descr')

    # ASSERT
    assert put_response.status_code == 400
    assert put_response.data == integrity_err_text

    test_util.teardown()


def test_sub_task_definitions():
    app = test_util.setup()
    ### TEST CREATE ###
    # ARRANGE
    # create checklist definition to be referenced
    cd_post_response = test_checklist_definition.post(app, 'cd_title', 'cd_descr')
    cd_id = cd_post_response.json['id']

    parent_title = 'test_task_definition_parent_title'
    parent_descr = 'test_task_definition_parent_descr'

    child_title = 'test_task_definition_child_title'
    child_descr = 'test_task_definition_child_descr'

    # ACT
    # create parent_task_definition
    parent_post_response = post(app=app,
                                title=parent_title,
                                checklist_definition_id=cd_id,
                                parent_task_definition_id=None,
                                description=parent_descr
                                )
    assert parent_post_response.status_code == 200
    parent_task_id = parent_post_response.json["id"]

    # create child_task_definition
    child_post_response = post(app=app,
                               title=child_title,
                               checklist_definition_id=None,
                               parent_task_definition_id=parent_task_id,
                               description=child_descr
                               )

    assert child_post_response.status_code == 200
    child_task_id = child_post_response.json["id"]

    # ASSERT
    # check parent get
    parent_get_response = get_by_id(app, parent_task_id)
    parent_get_response_json = parent_get_response.json
    assert parent_get_response.status_code == 200
    assert parent_get_response_json["title"] == parent_title
    assert parent_get_response_json["checklist_definition_id"] == cd_id
    assert parent_get_response_json["parent_task_definition_id"] is None
    assert parent_get_response_json["description"] == parent_descr
    assert len(parent_get_response_json["sub_task_definitions"]) == 1

    sub_task_def_json = parent_get_response_json["sub_task_definitions"][0]
    assert sub_task_def_json["id"] == child_task_id

    # check child get
    child_get_response = get_by_id(app, child_task_id)
    child_get_response_json = child_get_response.json
    assert child_get_response.status_code == 200
    assert child_get_response_json["title"] == child_title
    assert child_get_response_json["checklist_definition_id"] is None
    assert child_get_response_json["parent_task_definition_id"] == parent_task_id
    assert child_get_response_json["description"] == child_descr

    ### TEST CASCADING DELETE ###
    # ARRANGE

    # ACT
    parent_delete_response = delete(app=app, task_definition_id=parent_task_id)
    assert parent_delete_response.status_code == 200

    # ASSERT
    parent_get_response = get_by_id(app=app, task_definition_id=parent_task_id)
    assert parent_get_response.status_code == 404
    assert parent_get_response.json is None

    # ASSERT
    child_get_response = get_by_id(app=app, task_definition_id=child_task_id)
    assert child_get_response.status_code == 404
    assert child_get_response.json is None

    test_util.teardown()


def test_store_validation_relation():
    """tests the relation validations from the TaskDefinition Model"""
    app = test_util.setup()

    error_text = b'Task Definition always has to reference either a Checklist Definition or a Parent Task Definition'

    cd_post_response = test_checklist_definition.post(app, 'cd_title', 'cd_descr')
    cd_id = cd_post_response.json['id']

    title = 'test_task_definition_title'
    descr = 'test_task_definition_descr'

    ### both are None ###
    # ARRANGE
    # ACT
    post_response = post(app=app,
                         title=title,
                         checklist_definition_id=None,
                         parent_task_definition_id=None,
                         description=descr)

    # ASSERT
    assert post_response.status_code == 400
    assert post_response.data == error_text

    ### both are filled ###
    # ARRANGE
    parent_post_response = post(app=app,
                                title=title,
                                checklist_definition_id=cd_id,
                                parent_task_definition_id=None,
                                description=descr)

    parent_id = parent_post_response.json["id"]

    # ACT
    child_post_response = post(app=app,
                               title=title,
                               checklist_definition_id=cd_id,
                               parent_task_definition_id=parent_id,
                               description=descr)

    # ASSERT
    assert post_response.status_code == 400
    assert post_response.data == error_text

    test_util.teardown()


def test_store_validation_missing_parent():
    """tests self-referencing validation from the TaskDefinition Model"""
    app = test_util.setup()

    # ARRANGE
    error_text = b'The referenced TaskDefinition does not exist'

    cd_post_response = test_checklist_definition.post(app, 'cd_title', 'cd_descr')
    cd_id = cd_post_response.json['id']

    title = 'test_task_definition_title'
    descr = 'test_task_definition_descr'

    # ACT
    # create a task_definition that will try to reference itself as parent
    #   (hard-code parent_task_definition_id as 1 since this is the first one created since
    #    setup)
    post_response = post(app=app,
                         title=title,
                         checklist_definition_id=None,
                         parent_task_definition_id=1,
                         description=descr)

    # ASSERT
    assert post_response.status_code == 400
    assert post_response.data == error_text

    test_util.teardown()


def test_store_validation_circular_reference():
    """tests the circular reference validations from the TaskDefinition Model"""
    app = test_util.setup()

    # ARRANGE
    error_text = b'Circular Reference in TaskDefinition and its descendants is not allowed'

    cd_post_response = test_checklist_definition.post(app, 'cd_title', 'cd_descr')
    cd_id = cd_post_response.json['id']

    title = 'test_task_definition_title'
    descr = 'test_task_definition_descr'

    # set up a construct of parent-child-grandchild
    parent_post_response = post(app=app,
                                title=title,
                                checklist_definition_id=cd_id,
                                parent_task_definition_id=None,
                                description=descr)

    parent_id = parent_post_response.json["id"]

    child_post_response = post(app=app,
                               title=title,
                               checklist_definition_id=None,
                               parent_task_definition_id=parent_id,
                               description=descr)

    child_id = child_post_response.json["id"]

    grandchild_post_response = post(app=app,
                                    title=title,
                                    checklist_definition_id=None,
                                    parent_task_definition_id=child_id,
                                    description=descr)

    grandchild_id = grandchild_post_response.json["id"]

    # ACT / ASSERT
    # try to make the parent a child of its own child
    child_put_response = put(app=app,
                             task_definition_id=parent_id,
                             title=title,
                             description=descr,
                             parent_task_definition_id=child_id)
    assert child_put_response.status_code == 400
    assert child_put_response.data == error_text

    # try to make the parent a child of its own grandchild
    grandchild_put_response = put(app=app,
                                  task_definition_id=parent_id,
                                  title=title,
                                  description=descr,
                                  parent_task_definition_id=grandchild_id)
    assert grandchild_put_response.status_code == 400
    assert grandchild_put_response.data == error_text

    test_util.teardown()
