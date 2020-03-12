import json
from models import Base, add_user, create_user_task
from flask.cli import FlaskGroup
from app import app

cli = FlaskGroup(app)

@cli.command('reset-db')
def reset_db():
    Base.metadata.drop_all()
    Base.metadata.create_all()

@cli.command('fill-users')
def fill_users():
    with open('MOCK_USERS.json') as f:
        mock = json.load(f)
    for i in mock:
        add_user(**i)

@cli.command('fill-tasks')
def fill_tasks():
    with open('MOCK_TASKS.json') as f:
        mock = json.load(f)
    for i in mock:
        create_user_task(**i)


cli()
# reset_db()
# fill_db()