const MACHINE = [
  {
    type: 'category',
    label: 'Web',
    items: [
      'machine/web/asm',
      'machine/web/support',
      {
        type: 'category',
        label: 'Organizations',
        items: [
          'machine/web/organization/analytics-vulnerabilities',
          'machine/web/organization/analytics',
          'machine/web/organization/policies',
        ],
      },
      {
        type: 'category',
        label: 'Groups',
        items: [
          'machine/web/groups/vulnerabilities',
          'machine/web/groups/events',
          'machine/web/groups/stakeholders',
          'machine/web/groups/roles',
          'machine/web/groups/authors',
          {
            type: 'category',
            label: 'Scope',
            items: [
              'machine/web/groups/scope/introduction',
              'machine/web/groups/scope/roots',
              'machine/web/groups/scope/exclusions',
              'machine/web/groups/scope/files',
              'machine/web/groups/scope/portfolios',
            ],
          },
          'machine/web/groups/delete',
          'machine/web/groups/unsubscribe',
        ],
      },
      {
        type: 'category',
        label: 'Vulnerabilities',
        items: [
          {
            type: 'category',
            label: 'Management',
            items: [
              'machine/web/vulnerabilities/management/introduction',
              'machine/web/vulnerabilities/management/treatments',
              'machine/web/vulnerabilities/management/zero-risk',
              'machine/web/vulnerabilities/management/tracking',
            ],
          },
          {
            type: 'category',
            label: 'Creating new types of vulnerabilities',
            items: [
              'machine/web/vulnerabilities/new-vulnerability-types/create-draft',
              'machine/web/vulnerabilities/new-vulnerability-types/new-vuln-description',
              'machine/web/vulnerabilities/new-vulnerability-types/new-vuln-severity',
            ],
          },
          'machine/web/vulnerabilities/reporting-vulns',
          'machine/web/vulnerabilities/delete',
        ],
      },
    ],
  },
  {
    type: 'category',
    label: 'Scanner',
    items: [
      'machine/scanner/introduction',
      {
        type: 'category',
        label: 'Getting Started',
        items: [
          'machine/scanner/plans/introduction',
          'machine/scanner/plans/saas',
          'machine/scanner/plans/foss',
        ],
      },
      'machine/scanner/benchmark',
      'machine/scanner/reproducibility',
      'machine/scanner/results',
    ],
  },
  {
    type: 'category',
    label: 'Agent',
    items: [
      'machine/agent/introduction',
      'machine/agent/installation',
    ],
  },
  {
    type: 'category',
    label: 'API',
    items: [
      'machine/api/api-token',
      'machine/api/basics-api',
    ],
  },
]

module.exports = { MACHINE };
