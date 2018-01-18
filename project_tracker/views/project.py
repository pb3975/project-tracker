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

@project.route('/new', methods=['POST','GET'])
@login_required
def new():
    project = Project()
    form_project = model_form(Project,  field_args = {'title': {'label': 'Title'},'description': {'label': 'Project Description'},
                                                         'primary_language': {'label':'Primary Programming Language'}, 'tools': {'label':'Other Tools'}, 'slug': {'label':'Unique Project Name'},
                                                         'repo': {'label':'GitHub Repository'}, 'location_url': {'label': 'Hosted Link'},'status': {'label':'Status'}}, 
                                                         exclude=('slug', 'startDate', 'endDate', 'createdDate', 'notes', 'closed', 'week_completed', 'minutes_worked', 'owner'))
    form = form_project(request.form)
    return render_template('projects/create.html', form=form)


@project.route('/create', methods=['POST'])
@login_required
def create():
    public = False    
    if request.form.get(public) == 'y':
        public = True
    else:
        public = False

    project = Project()
    project.title = request.form['title']
    project.public = public
    project.description = request.form['description']
    project.primary_language = request.form.get('primary_language')
    project.tools = request.form.get('tools')
    project.status = request.form['status']
    project.repo = request.form.get('repo')
    project.sources = request.form.get('sources')
   
    project.owner = current_user.id
    project.save()
    _id = project.id

    return render_template('projects/detail.html',project=project)


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

