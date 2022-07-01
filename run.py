"""CheckThis app"""
from checkthis import app
from checkthis import db

# Run App
if __name__ == "__main__":
    app.run(debug=True)
    # from checkthis.models import ChecklistDefinition TODO maybe this works??
    db.create_all()
    # TODO At the moment, this does not actually create the tables.
    # (maybe because the models are not loaded at creation time of the 'db' variable.)
    # Workaround: manually create the tables by running flask in the terminal, import db as well as the models,
    #             and db.create_all() from there
