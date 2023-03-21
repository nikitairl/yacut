import random
import string
from datetime import datetime

from . import db


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(255), nullable=False)
    short = db.Column(db.String(5), nullable=False, unique=True, index=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    @classmethod
    def available_short(cls, short_id):
        return cls.query.filter_by(short=short_id).first() is None

    @classmethod
    def get_unique_short_id(cls):
        letters= string.ascii_lowercase + string.ascii_uppercase
        while True:
            random_letters = random.choices(letters, k=5)
            short_id = ''.join(random_letters)
            if cls.available_short(short_id):
                break
        return short_id
            
            