from checkthis.models import TaskDefinition
from checkthis.models import ChecklistDefinition


def test_new_checklist_definition():
    test_title = 'test_title'
    test_description = 'test_description'

    cd = ChecklistDefinition(title=test_title, description=test_description)
    assert cd.title == test_title
    assert cd.description == test_description


def test_new_task_definition():
    test_title = 'test_title'
    test_description = 'test_description'

    td = TaskDefinition(title=test_title, description=test_description)
    assert td.title == test_title
    assert td.description == test_description
