from flask import Blueprint, request, redirect, render_template, url_for
from flask.views import MethodView
from flask_mongoengine.wtf import model_form
from project_tracker.auth import requires_auth
from project_tracker.models import Project, Note
from flask_login import current_user, login_required

admin = Blueprint('admin', __name__, template_folder='templates')


class List(MethodView):
    decorators = [requires_auth]
    cls = Project

    def get(self):
        projects = self.cls.objects.all()
        return render_template('admin/list.html', projects=projects)




class Detail(MethodView):


    def get_context(self, _id=None):

        if _id:
            project = Project.objects.get_or_404(id=_id)
            form_project = model_form(Project,  field_args = {'title': {'label': 'Title'},'description': {'label': 'Project Description'},
                                                 'primary_language': {'label':'Primary Programming Language'}, 'tools': {'label':'Other Tools'},
                                                 'repo': {'label':'GitHub Repository'}, 'location_url': {'label': 'Hosted Link'},'status': {'label':'Status'}, 'sources': {'label': 'Sources Used'}}, 
                                                 exclude=('slug', 'minutes_worked'))

            if request.method == 'POST':
                form = form_project(request.form, inital=project._data)
            else:
                form = form_project(obj=project)
        else:
            project = Project()
            form_project = model_form(Project,  field_args = {'title': {'label': 'Title'},'description': {'label': 'Project Description'},
                                                             'primary_language': {'label':'Primary Programming Language'}, 'tools': {'label':'Other Tools'}, 'slug': {'label':'Unique Project Name'},
                                                             'repo': {'label':'GitHub Repository'}, 'location_url': {'label': 'Hosted Link'},'status': {'label':'Status'}}, 
                                                             exclude=('slug', 'startDate', 'endDate', 'createdDate', 'notes', 'closed', 'week_completed', 'minutes_worked', 'owner'))
            form = form_project(request.form)
        context = {
            "project": project,
            "form": form,
            "create": _id is None
        }
        return context
    @login_required
    def get(self, _id):
        context = self.get_context(_id)
        return render_template('admin/detail.html', **context)
    @login_required
    def post(self, _id):
        context = self.get_context(_id)
        form = context.get('form')

        if form.validate():

            project = context.get('project')
            form.populate_obj(project)
            project.owner = current_user.id
            project.save()

            return redirect(url_for('projects.home'))
        return render_template('admin/detail.html', **context)

# Register the urls
admin.add_url_rule('/admin/', view_func=List.as_view('index'))
admin.add_url_rule('/create/', defaults={'_id': None}, view_func=Detail.as_view('create'))
admin.add_url_rule('/<_id>/', view_func=Detail.as_view('edit'))

decorators = [requires_auth]
@admin.route('/admin/delete/<_id>', methods=['POST', 'GET'])
@login_required
def remove(_id):
    project = Project.objects.get_or_404(id=_id)
    project.delete()
    return redirect(url_for('admin.index'))

