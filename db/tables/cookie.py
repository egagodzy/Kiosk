from db.config import sqlalchemy


metadata = sqlalchemy.MetaData()
cookie = sqlalchemy.Table(
    "cookie",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("usercookie", sqlalchemy.String),
    sqlalchemy.Column("username", sqlalchemy.String),
)