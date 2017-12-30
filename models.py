import datetime
from flask import url_for
from app import db


class Note(db.EmbeddedDocument):
	publishedDate = db.DateTimeField(default=datetime.datetime.now)
	body = db.StringField()

class Project(db.Document):
	title = db.StringField(max_length=90, required=True)
	slug = db.StringField(max_length=255, required=True)
	description = db.StringField(required=True)
	createdDate = db.DateTimeField(default=datetime.datetime.now, required=True)
	startDate = db.DateTimeField()
	endDate = db.DateTimeField()
	closed = db.BooleanField()
	primary_language = db.StringField()
	tools = db.StringField()
	repo = db.URLField()
	location_url = db.URLField()
	week_completed = db.IntField()
	status = db.StringField(default='New', required=True)
	notes = db.ListField(db.EmbeddedDocumentField('Note'))

	def get_absolute_url(self):
		return url_for('project', kwargs={"slug": self.slug})

	def __unicode__(self):
		return self.title 

	meta = { 
	    'allow_inheretence': True,
	    'indexes': ['-createdDate', 'slug'],
	    'ordering': ['createdDate']
	   }




