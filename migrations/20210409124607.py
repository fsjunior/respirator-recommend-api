"""
Migration description here!
"""
name = '20210409124607'
dependencies = ['20210405143815']


def upgrade(db: "pymongo.database.Database"):
    db["approval_certificate"].create_index([("number", 1)])
    db["respirator"].create_index([("url", 1)])
    db["respirator"].create_index([("date", -1)], expireAfterSeconds=172800)


def downgrade(db: "pymongo.database.Database"):
    db["approval_certificate"].drop_index("number_1")
    db["respirator"].drop_index("url_1")
    db["respirator"].drop_index("date_-1")
    pass

