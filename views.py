from flask import Blueprint, request, redirect, render_template, url_for
from flask.views import MethodView

from flask_mongoengine.wtf import model_form
from models import Project, Note

projects = Blueprint('projects', __name__, template_folder='templates')


class ListView(MethodView):

    def get(self): 
        projects = Project.objects.all()
        return render_template('projects/list.html', projects=projects)


class DetailView(MethodView):

    form = model_form(Note, field_args= {'body' :{'label': 'Write your note here...'}})

    def get_context(self, slug):
        project = Project.objects.get_or_404(slug=slug)
        form = self.form(request.form)

        context = {
            "project": project,
            "form": form
        }
        return context

    def get(self, slug):
        context = self.get_context(slug)
        return render_template('projects/detail.html', **context)

    def post(self, slug):
        context = self.get_context(slug)
        form = context.get('form')

        if form.validate():
            note = Note()
            form.populate_obj(note)

            project = context.get('project')
            project.notes.append(note)
            project.save()

            return redirect(url_for('projects.detail', slug=slug))
        return render_template('projects/detail.html', **context)

projects.add_url_rule('/', view_func=ListView.as_view('list'))
projects.add_url_rule('/<slug>/', view_func=DetailView.as_view('detail'))
