from graphene import ObjectType, List, String
from backend.entity.project import Project
from backend.domain import project as project_domain


class Tag(ObjectType):

    name = String()
    projects = List(Project)

    def __init__(self, tag, user_projects):
        super(Tag, self).__init__()
        self.name = tag
        projects = []
        for project in user_projects:
            project_tag = project_domain.get_attributes(
                project, ['tag']).get('tag', [])
            project_tag = [proj_tag.lower() for proj_tag in project_tag]
            if tag in project_tag:
                projects.append(project.lower())
        projects_list = [Project(project, description=project_domain.get_description(project))
                         for project in projects]
        self.projects = projects_list

    def resolve_name(self, info):
        """Resolve name attribute."""
        del info
        return self.name
