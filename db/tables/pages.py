from db.config import sqlalchemy


metadata = sqlalchemy.MetaData()
pages = sqlalchemy.Table(
    "pages",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("pagename", sqlalchemy.String),
    sqlalchemy.Column("pagetype", sqlalchemy.String),
    sqlalchemy.Column("pageicon", sqlalchemy.String),
    sqlalchemy.Column("pagetitle", sqlalchemy.String),
    sqlalchemy.Column("pagebody", sqlalchemy.String),
    sqlalchemy.Column("pagenav", sqlalchemy.String),
    sqlalchemy.Column("pagesrc", sqlalchemy.String),
)