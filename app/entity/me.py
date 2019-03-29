from graphene import ObjectType, String

from app.util import get_jwt_content
from app.services import is_customeradmin


class Me(ObjectType):
    role = String(project_name=String(required=False))

    def resolve_role(self, info, project_name=None):
        jwt_content = get_jwt_content(info.context)
        role = jwt_content.get('user_role')
        if project_name and role == 'customer':
            email = jwt_content.get('user_email')
            role = 'customeradmin' if is_customeradmin(project_name, email) else 'customer'
        self.role = role

        return self.role
