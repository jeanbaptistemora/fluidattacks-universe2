from graphene import ObjectType, List, String

from app.util import get_jwt_content
from app.services import is_customeradmin
from app.entity.project import Project
from app.dao import integrates_dao


class Me(ObjectType):
    role = String(project_name=String(required=False))
    projects = List(Project)

    def __init__(self):
        super(Me, self).__init__()
        self.role = ''
        self.projects = []

    def resolve_role(self, info, project_name=None):
        jwt_content = get_jwt_content(info.context)
        role = jwt_content.get('user_role')
        if project_name and role == 'customer':
            email = jwt_content.get('user_email')
            role = 'customeradmin' if is_customeradmin(
                project_name, email) else 'customer'
        self.role = role

        return self.role

    def resolve_projects(self, info):
        jwt_content = get_jwt_content(info.context)
        user_email = jwt_content.get('user_email')
        for project in integrates_dao.get_projects_by_user(user_email):
            self.projects.append(
                Project(project_name=project[0], description=project[1])
            )

        return self.projects
