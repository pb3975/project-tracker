from flask import Blueprint, request, redirect, render_template, url_for
from flask.views import MethodView
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_mongoengine.wtf import model_form
from project_tracker.models import Project, Note, User

project = Blueprint('projects', __name__, template_folder='templates')


@project.route('/', methods=['POST','GET'])
def home(): 
    projects = Project.objects(public=True)
    # projects = Project.objects.all()
    return render_template('projects/list.html', projects=projects)


class DetailView(MethodView):

    form = model_form(Note, field_args={'body' :{'label': 'Write your comment here...'}}, exclude=['publishedDate', 'author'])
    @login_required
    def get_context(self, _id):
        project = Project.objects.get_or_404(id=_id)
        form = self.form(request.form)

        context = {
            "project": project,
            "form": form
        }
        return context
    @login_required
    def get(self, _id):
        context = self.get_context(_id)
        return render_template('projects/detail.html', **context)
    @login_required
    def post(self, _id):
        context = self.get_context(_id)
        form = context.get('form')

        if form.validate():
            note = Note()
            form.populate_obj(note)
            note.author = current_user.id

            project = context.get('project')
            project.notes.append(note)
            project.save()

            return redirect(url_for('projects.detail', _id=_id))
        return render_template('projects/detail.html', **context)
project.add_url_rule('/<_id>/', view_func=DetailView.as_view('detail'))

