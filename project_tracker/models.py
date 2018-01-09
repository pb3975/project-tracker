import datetime
from flask import url_for
from flask_login import UserMixin
from project_tracker import db, bcrypt
from flask_mongoengine import MongoEngine


# db = MongoEngine(app)


class User(db.Document):
	email = db.EmailField(required=True)
	password = db.StringField(required=True, max=80)
	createdDate = db.DateTimeField(default=datetime.datetime.now, required=True)
	username = db.StringField(required=True, max=80)
	authenticated = db.BooleanField(default=False)

	def __repr__(self):
		return '<User %r>' % self.email
	def is_authenticated(self):
		return True
	def is_active(self):
		return True
	def is_anonymous(self):
		return False
	def get_id(self):
		return str(self.email)

	meta = { 
	    'allow_inheretence': True,
	    'indexes': ['-createdDate', 'email'],
	    'ordering': ['createdDate']
	   }



	

class Note(db.EmbeddedDocument):
	publishedDate = db.DateTimeField(default=datetime.datetime.now)
	body = db.StringField(required=True)
	author = db.ReferenceField(User)

class Project(db.Document):
	title = db.StringField(max_length=90, required=True)
	slug = db.StringField(max_length=255)
	owner = db.ReferenceField(User)
	public = db.BooleanField(default=False)
	description = db.StringField(required=True)
	createdDate = db.DateTimeField(default=datetime.datetime.now, required=True)
	startDate = db.DateTimeField()
	endDate = db.DateTimeField()
	closed = db.BooleanField()
	primary_language = db.StringField(max_length=55)
	tools = db.StringField()
	repo = db.URLField()
	location_url = db.URLField()
	week_completed = db.IntField()
	status = db.StringField(default='New', required=True)
	sources = db.StringField()
	notes = db.ListField(db.EmbeddedDocumentField('Note'))
	minutes_worked = db.IntField(default=0)

	def get_absolute_url(self):
		return url_for('project', kwargs={"id": self.id})

	def __unicode__(self):
		return self.title 

	meta = { 
	    'allow_inheretence': True,
	    'indexes': ['-createdDate', 'slug'],
	    'ordering': ['createdDate']
	   }




