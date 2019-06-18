from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import scoped_session, sessionmaker
from .extensions import db

class Notes(db.Model):
    __tablename__ = 'notes'
    id = db.Column(Integer, primary_key=True)
    content = db.Column(String(255), unique=True)
    title = db.Column(String(255), unique=True)
    created_at = db.Column(DateTime())
    updated_at = db.Column(DateTime())

    def __init__(self):
        self.title = ""
        self.content = ""

    def __repr__(self):
        return '<Note %r>' % (self.title)