"""Models"""

from checkthis import db
from checkthis import ma


class TaskDefinition(db.Model):
    """Class TaskDefinition"""
    id = db.Column(db.Integer, primary_key=True)
    checklist_definition_id = db.Column(db.Integer, db.ForeignKey('checklist_definition.id'))
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(1000))

    def __repr__(self):
        return f"TaskDefinition(ID: '{self.id}', Checklist Definition ID: '{self.checklist_definition_id}', Title: {self.title}', Description: '{self.description}' "


class TaskDefinitionSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ('id', 'checklist_definition_id', 'title', 'description')
        model = TaskDefinition


task_definition_schema = TaskDefinitionSchema()
task_definitions_schema = TaskDefinitionSchema(many=True)


class ChecklistDefinition(db.Model):
    """Class ChecklistDefinition"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(1000))
    task_definitions = db.relationship('TaskDefinition', backref='checklist_definition', lazy=True)

    def __repr__(self):
        return f"ChecklistDefinition('{self.id}', '{self.title}', '{self.description}' '{self.task_definitions}'"


class ChecklistDefinitionSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ('id', 'task_definitions', 'title', 'description')
        model = ChecklistDefinition

    task_definitions = ma.Nested(TaskDefinitionSchema, many=True)


checklist_definition_schema = ChecklistDefinitionSchema()
checklist_definitions_schema = ChecklistDefinitionSchema(many=True)
