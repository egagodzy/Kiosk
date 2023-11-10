import databases
import sqlalchemy
from db.tables.users import *
from db.tables.cookie import *
from db.tables.pages import *
from db.tables.main_page import *

DATABASE_URL = "sqlite:///db/kiosk.db"

database = databases.Database(DATABASE_URL)

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

main_page = sqlalchemy.Table(
    "main_page",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("pagename", sqlalchemy.String),
)


users = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("username", sqlalchemy.String),
    sqlalchemy.Column("userpassword", sqlalchemy.String),
)


cookie = sqlalchemy.Table(
    "cookie",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("usercookie", sqlalchemy.String),
    sqlalchemy.Column("username", sqlalchemy.String),
)

engine = sqlalchemy.create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
metadata.create_all(engine)