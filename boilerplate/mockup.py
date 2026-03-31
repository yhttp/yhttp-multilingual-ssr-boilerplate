from .auth import mockup as auth_mockup
from .shop import mockup as shop_mockup


def insert(db):
    print(f'generating mockup data, db url: {db.engine.url}')
    auth_mockup.insert(db)
    shop_mockup.insert(db)
    print('mockup data generation done')
