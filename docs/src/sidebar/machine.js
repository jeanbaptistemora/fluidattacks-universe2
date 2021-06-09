const MACHINE = [
  {
    type: 'category',
    label: 'App',
    items: [
      'machine/app/asm',
      'machine/app/support',
      {
        type: 'category',
        label: 'Organizations',
        items: [
          'machine/app/organization/analytics-vulnerabilities',
          'machine/app/organization/analytics',
          'machine/app/organization/policies',
        ],
      },
      {
        type: 'category',
        label: 'Groups',
        items: [
          'machine/app/groups/vulnerabilities',
          'machine/app/groups/events',
          'machine/app/groups/stakeholders',
          'machine/app/groups/roles',
          'machine/app/groups/authors',
          {
            type: 'category',
            label: 'Scope',
            items: [
              'machine/app/groups/scope/introduction',
              'machine/app/groups/scope/roots',
              'machine/app/groups/scope/exclusions',
              'machine/app/groups/scope/files',
              'machine/app/groups/scope/portfolios',
            ],
          },
          'machine/app/groups/delete',
          'machine/app/groups/unsubscribe',
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
              'machine/app/vulnerabilities/management/introduction',
              'machine/app/vulnerabilities/management/treatments',
              'machine/app/vulnerabilities/management/zero-risk',
              'machine/app/vulnerabilities/management/tracking',
            ],
          },
          {
            type: 'category',
            label: 'Creating new types of vulnerabilities',
            items: [
              'machine/app/vulnerabilities/new-vulnerability-types/create-draft',
              'machine/app/vulnerabilities/new-vulnerability-types/new-vuln-description',
              'machine/app/vulnerabilities/new-vulnerability-types/new-vuln-severity',
            ],
          },
          'machine/app/vulnerabilities/reporting-vulns',
          'machine/app/vulnerabilities/delete',
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
