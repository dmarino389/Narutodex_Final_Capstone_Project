from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

# Assuming you want a many-to-many relationship
user_characters = db.Table('user_characters',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('character_id', db.Integer, db.ForeignKey('character.id'), primary_key=True)
)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    character_collection = db.relationship('Character', secondary=user_characters, backref=db.backref('users', lazy='dynamic'))
    wins = db.Column(db.Integer, default=0)
    losses = db.Column(db.Integer, default=0)

    def add_win(self):
        self.wins += 1
        db.session.commit()

    def add_loss(self):
        self.losses += 1
        db.session.commit()

    @property
    def user_pokemon(self):
        return [Character.query.get(user_character.character_id) for user_character in self.character_collection]

class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    hp = db.Column(db.Integer, nullable=True)
    attack = db.Column(db.Integer, nullable=False)
    defense = db.Column(db.Integer, nullable=False)
    sprite = db.Column(db.String(500), nullable=True)  # Assuming sprite is a URL, so the String length is set to 500.
    abilities = db.Column(db.String(255), nullable=True)  # Storing abilities as comma-separated values.
