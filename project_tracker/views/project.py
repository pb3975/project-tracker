from flask import Blueprint, request, redirect, render_template, url_for
from flask.views import MethodView
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_mongoengine.wtf import model_form
from project_tracker.models import Project, Note, User

project = Blueprint('projects', __name__, template_folder='templates')


@project.route('/', methods=['POST','GET'])
def home(): 
    # projects = Project.objects(public=True)
    projects = Project.objects.all()
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

# project.add_url_rule('/', view_func=ListView.as_view('list'))
project.add_url_rule('/<_id>/', view_func=DetailView.as_view('detail'))

# @project.route('/<_id>', methods=['GET', 'POST'])
# @login_required
# def detail(_id):
#     form = model_form(Note, field_args={'body' :{'label': 'Write your comment here...'}}, exclude=['publishedDate'])
#     project = Project.objects.get_or_404(id=_id)

    
#     return render_template('projects/detail.html', project=project)

#     def post(self, id):

#         if form.validate():
#             note = Note()
#             form.populate_obj(note)

#             project.notes.append(note)
#             project.save()

#             return redirect(url_for('projects.detail', id=_id, form=form))
#         return render_template('projects/detail.html', project=project)

# @project.route('/new/', methods=['GET', 'POST'])
# @login_required
# def new():
#     project = Project()

#     form_project = model_form(Project,  field_args = {'title': {'label': 'Title'},'description': {'label': 'Project Description'},
#                                                  'primary_language': {'label':'Primary Programming Language'}, 'tools': {'label':'Other Tools'}, 'slug': {'label':'Unique Project Name'},
#                                                  'repo': {'label':'GitHub Repository'}, 'location_url': {'label': 'Hosted Link'},'status': {'label':'Status'}}, 
#                                                  exclude=('startDate', 'endDate', 'createdDate', 'notes', 'closed', 'week_completed', 'minutes_worked', 'owner'))
#     form = form_project(request.form)
#     context = {
#     "project": project,
#     "form": form,
#     }
#     if form.validate_on_submit():
#         # project = context.get('project')
#         form.populate_obj(project)
#         project.save()    
        
#         return redirect(url_for('projects.home'))
#     return render_template('projects/create.html', form=form)
