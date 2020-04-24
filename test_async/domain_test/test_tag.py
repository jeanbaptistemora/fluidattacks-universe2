from django.test import TestCase
from backend.dal import tag as tag_dal
from backend.domain import project as project_domain
from backend.domain.tag import update_organization_indicators


class TagTest(TestCase):

    def test_update_organization_indicators(self):
        projects = project_domain.get_active_projects()
        projects = [project_domain.get_attributes(project, ['companies', 'project_name', 'tag'])
                for project in projects]
        assert update_organization_indicators('fluid', projects)
        tag_info = tag_dal.get('fluid', 'test-projects')
        assert tag_info['mean_remediate_low_severity'] == 116
