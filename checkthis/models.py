'''Models'''
from checkthis import db

class TaskDefinition(db.Model):
    '''Class TaskDefinition'''
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), nullable = False)

    def __repr__(self):
        return f"TaskDefinition('{self.id}', '{self.title}'"
