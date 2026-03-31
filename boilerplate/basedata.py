from .common import basedata as common_basedata
from .auth import basedata as auth_basedata


def insert(db):
    common_basedata.insert(db)
    auth_basedata.insert(db)
