from flask import Blueprint, request, redirect, render_template, url_for
from flask.views import MethodView

from flask_mongoengine.wtf import model_form

from project_tracker.auth import requires_auth
from project_tracker.models import Project, Note

admin = Blueprint('admin', __name__, template_folder='templates')


class List(MethodView):
    decorators = [requires_auth]
    cls = Project

    def get(self):
        projects = self.cls.objects.all()
        return render_template('admin/list.html', projects=projects)


class Detail(MethodView):

    decorators = [requires_auth]

    def get_context(self, slug=None):

        if slug:
            project = Project.objects.get_or_404(slug=slug)
            form_project = model_form(Project,  field_args = {'title': {'label': 'Title'},'description': {'label': 'Project Description'},
                                                 'primary_language': {'label':'Primary Programming Language'}, 'tools': {'label':'Other Tools'},
                                                 'repo': {'label':'GitHub Repository'}, 'location_url': {'label': 'Hosted Link'},'status': {'label':'Status'}}, 
                                                 exclude=('slug'))

            if request.method == 'POST':
                form = form_project(request.form, inital=project._data)
            else:
                form = form_project(obj=project)
        else:
            project = Project()
            form_project = model_form(Project,  field_args = {'title': {'label': 'Title'},'description': {'label': 'Project Description'},
                                                             'primary_language': {'label':'Primary Programming Language'}, 'tools': {'label':'Other Tools'}, 'slug': {'label':'Unique Project Name'},
                                                             'repo': {'label':'GitHub Repository'}, 'location_url': {'label': 'Hosted Link'},'status': {'label':'Status'}}, 
                                                             exclude=('startDate', 'endDate', 'createdDate', 'notes', 'closed', 'week_completed'))
            form = form_project(request.form)
        context = {
            "project": project,
            "form": form,
            "create": slug is None
        }
        return context

    def get(self, slug):
        context = self.get_context(slug)
        return render_template('admin/detail.html', **context)

    def post(self, slug):
        context = self.get_context(slug)
        form = context.get('form')

        if form.validate():
            project = context.get('project')
            form.populate_obj(project)
            project.save()

            return redirect(url_for('admin.index'))
        return render_template('admin/detail.html', **context)


# Register the urls
admin.add_url_rule('/admin/', view_func=List.as_view('index'))
admin.add_url_rule('/admin/create/', defaults={'slug': None}, view_func=Detail.as_view('create'))
admin.add_url_rule('/admin/<slug>/', view_func=Detail.as_view('edit'))