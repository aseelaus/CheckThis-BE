"""Models"""

from checkthis import db
from checkthis import ma
from checkthis.errors import TaskDefinitionRelationError, TaskDefinitionMissingParentError, \
    TaskDefinitionCircularReferenceError


class TaskDefinition(db.Model):
    """Class TaskDefinition"""
    id = db.Column(db.Integer, primary_key=True)
    checklist_definition_id = db.Column(db.Integer, db.ForeignKey('checklist_definition.id'))
    parent_task_definition_id = db.Column(db.Integer, db.ForeignKey('task_definition.id'))
    sub_task_definitions = db.relationship('TaskDefinition',
                                           backref=db.backref('parent',
                                                              remote_side=[id]
                                                              ),
                                           lazy=True,
                                           cascade="all, delete-orphan")
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(1000))

    def __repr__(self):
        return f"TaskDefinition(ID: '{self.id}', " \
               f"Checklist Definition ID: '{self.checklist_definition_id}', " \
               f"Title: {self.title}', " \
               f"Description: '{self.description}'"

    def validate_store(self):
        """Validate some application specific logic and store the object in the database"""

        # VALIDATIONS
        # TaskDefinition always has to relate to either a parent-TaskDefinition or a ChecklistDefinition
        if self.checklist_definition_id is None and self.parent_task_definition_id is None:
            raise TaskDefinitionRelationError
        if self.checklist_definition_id is not None and self.parent_task_definition_id is not None:
            raise TaskDefinitionRelationError
        # TaskDefinition cannot be its own parent.
        # Since self.id is not populated before db commit, it cannot be
        # compared to self.parent_task_definition_id here. as a workaround, explicitly check if the
        # parent_task_definition exists in the db at this point.
        if self.parent_task_definition_id is not None and \
                TaskDefinition.query.get(self.parent_task_definition_id) is None:
            raise TaskDefinitionMissingParentError

        # no circular relationship between task-definitions
        # parent cannot be one of the tasks descendants
        def check_child_circular_references(child, parent_task_definition_id):
            """recursively checks if a new parent_task_definition is already a descendant of the TaskDefinition"""
            if child.id == parent_task_definition_id:
                raise TaskDefinitionCircularReferenceError
            for grandchild in child.sub_task_definitions:
                check_child_circular_references(grandchild, parent_task_definition_id)

        if self.parent_task_definition_id is not None:
            for c in self.sub_task_definitions:
                check_child_circular_references(c, self.parent_task_definition_id)

        # STORE AND COMMIT
        db.session.add(self)
        db.session.commit()


class TaskDefinitionSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = (
            'id',
            'title',
            'description',
            'checklist_definition_id',
            'parent_task_definition_id',
            'sub_task_definitions'
        )
        model = TaskDefinition

    sub_task_definitions = ma.Nested(lambda: TaskDefinitionSchema, many=True)


task_definition_schema = TaskDefinitionSchema()
task_definitions_schema = TaskDefinitionSchema(many=True)


class ChecklistDefinition(db.Model):
    """Class ChecklistDefinition"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(1000))
    task_definitions = db.relationship('TaskDefinition',
                                       backref='checklist_definition',
                                       lazy=True,
                                       cascade="all, delete-orphan")

    def __repr__(self):
        return f"ChecklistDefinition('{self.id}', '{self.title}', '{self.description}' '{self.task_definitions}'"


class ChecklistDefinitionSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ('id', 'title', 'description', 'task_definitions')
        model = ChecklistDefinition

    task_definitions = ma.Nested(TaskDefinitionSchema, many=True)


checklist_definition_schema = ChecklistDefinitionSchema()
checklist_definitions_schema = ChecklistDefinitionSchema(many=True)
