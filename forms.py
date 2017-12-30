from flask_mongoengine.wtf import model_form
from models import Project

ProjectForm = model_form(Project)
