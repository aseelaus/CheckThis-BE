from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

# registers routes and models to the app. must be below definition of variable "db" to avoid circular imports
from checkthis import routes
from checkthis.models import ChecklistDefinition
from checkthis.models import TaskDefinition
