from checkthis import create_app, db

test_database_uri = 'sqlite:///test_db.sqlite'


def setup():
    app = create_app(test_database_uri)
    app.testing = True
    app.app_context().push()
    db.create_all()
    return app


def teardown():
    db.session.remove()
    db.drop_all()
