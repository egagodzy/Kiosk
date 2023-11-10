from db.config import sqlalchemy


metadata = sqlalchemy.MetaData()
main_page = sqlalchemy.Table(
    "main_page",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("pagename", sqlalchemy.String),
)