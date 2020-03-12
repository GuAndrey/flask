import json
from model import Base, add_user
from flask.cli import FlaskGroup
from app import app

cli = FlaskGroup(app)

@cli.command('reset-db')
def reset_db():
    Base.metadata.drop_all()
    Base.metadata.create_all()

@cli.command('fill-users')
def fill_users():
    with open('MOCK_DATA.json') as f:
        mock = json.load(f)
    for i in mock:
        add_user(**i)

@cli.command('fill-tasks')
def fill_tasks():
    

cli()
# reset_db()
# fill_db()