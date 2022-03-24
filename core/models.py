"""Data models."""
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


class Channel(db.Model):
    """ Data model for channel """
    __tablename__ = 'channel'
    id = db.Column(db.Integer(), autoincrement=True, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    title = db.Column(db.String(), nullable=False)
    timezone = db.Column(db.String(), nullable=False)

    def __repr__(self):
        return '{}'.format(self.name)


class Program(db.Model):
    """ Data model for program """
    __tablename__ = 'program'
    id = db.Column(db.Integer(), autoincrement=True, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    title = db.Column(db.String(), nullable=False)
    description = db.Column(db.String(), nullable=False)
    genre = db.Column(db.String(), server_default='music')
    rating = db.Column(db.String(), server_default='nr')

    # add to_dict() method so that we can serialized to JSON (e.g needed for ajax)
    def to_dict(self):
        return {
            'name': self.name,
            'title': self.title,
            'description': self.description,
            'genre': self.genre,
            'rating': self.rating
        }

    def __repr__(self):
        return '{}'.format(self.name)


class Schedule(db.Model):
    """" Data model for schedule """
    __tablename__ = 'schedule'
    id = db.Column(db.Integer(), autoincrement=True, primary_key=True)
    program_id = db.Column(db.Integer(), db.ForeignKey('program.id'), nullable=False)
    channel_id = db.Column(db.Integer(), db.ForeignKey('channel.id'), nullable=False)
    start = db.Column(db.TIMESTAMP(), nullable=False)
    end = db.Column(db.TIMESTAMP(), nullable=False)

    def __repr__(self):
        return 'id:{}, program_id:{}, channel_id:{}'.format(self.id, self.program_id, self.channel_id)


class Template(db.Model):
    """ Data model for template """
    __tablename__ = 'template'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(), nullable=False)
    description = db.Column(db.String(), nullable=False)

    def __repr__(self):
        return '{}'.format(self.name)


class TemplateList(db.Model):
    """ Data model for template_list """
    __tablename__ = 'template_list'
    id = db.Column(db.Integer(), db.ForeignKey('template.id'), autoincrement=True, primary_key=True)
    schedule_id = db.Column(db.Integer(), db.ForeignKey('schedule.id'), nullable=False, unique=True)

    def __repr__(self):
        return 'id:{}, schedule_id:{}'.format(self.id, self.schedule_id)