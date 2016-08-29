from server import create_session
from server import engine
from server import Excuse


def initialize_database_for_model(model):
    model.metadata.create_all(engine)


def load_excuses():
    """load, specifically and only, the excuses fixtures. all hard coded.
    i'm not ashamed"""
    db_session = create_session()
    with open("fixtures/excuses.txt", 'r') as file:
        for line in file:
            excuse = Excuse(line.rstrip("\n"))
            excuse.published = True
            db_session.add(excuse)
    db_session.commit()
