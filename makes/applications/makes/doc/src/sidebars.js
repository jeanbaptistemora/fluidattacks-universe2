function getDocs(path) {
  var fs = require('fs');
  var files = fs.readdirSync(`docs/${path}`)

  files.forEach(
    function prepareFile(item, index, arr) {
      arr[index] = `${path}/${item.replace('.md', '')}`
    }
  )

  return files
}

module.exports = {
  Web: [
    'web/asm',
    {
      type: 'category',
      label: 'Manage your organization',
      items: [
        'web/organization/analytics-vulnerabilities',
        'web/organization/analytics-generic',
      ],
    },
    {
      type: 'category',
      label: 'Manage your groups',
      items: [
        'web/groups/vulnerabilities',
        'web/groups/consulting',
        {
          type: 'category',
          label: 'Scope',
          items: [
            'web/groups/scope/introduction',
            'web/groups/scope/gitroots',
            'web/groups/scope/files',
            'web/groups/scope/portfolio',
          ],
        },
        'web/groups/deleting-unsubscribing',
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
            'web/vulnerabilities/management/introduction',
            'web/vulnerabilities/management/treatments',
            'web/vulnerabilities/management/reattacks',
            'web/vulnerabilities/management/tracking',
          ],
        },
        {
          type: 'category',
          label: 'Creating new types of vulnerabilities',
          items: [
            'web/vulnerabilities/new-vulnerability-types/create-draft',
            'web/vulnerabilities/new-vulnerability-types/new-vuln-description',
            'web/vulnerabilities/new-vulnerability-types/new-vuln-severity',
          ],
        },
        'web/vulnerabilities/reporting-vulns',
      ],
    },
    'web/glossary',
  ],
  Mobile: {
    Mobile: getDocs('mobile'),
  },
  API: [
    'api/api-token',
    'api/basics-api',
  ],
  Requirements: [
    'requirements/intro',
    {
      type: 'category',
      label: 'Credentials',
      items: [
        'requirements/credentials/r126',
        'requirements/credentials/r127',
        'requirements/credentials/r128',
        'requirements/credentials/r129',
        'requirements/credentials/r130',
        'requirements/credentials/r131',
        'requirements/credentials/r132',
        'requirements/credentials/r133',
        'requirements/credentials/r134',
        'requirements/credentials/r135',
        'requirements/credentials/r136',
        'requirements/credentials/r137',
        'requirements/credentials/r138',
        'requirements/credentials/r139',
        'requirements/credentials/r140',
        'requirements/credentials/r141',
        'requirements/credentials/r142',
        'requirements/credentials/r143',
        'requirements/credentials/r144',
        'requirements/credentials/r332',
        'requirements/credentials/r333',
      ],
    },
    {
      type: 'category',
      label: 'Authentication',
      items: [
        'requirements/authentication/r122',
        'requirements/authentication/r153',
        'requirements/authentication/r225',
      ],
    },
    {
    type: 'category',
      label: 'Authorization',
      items: [
        'requirements/authorization/r033',
        'requirements/authorization/r034',
        'requirements/authorization/r035',
      ],
    },
    {
      type: 'category',
        label: 'Session',
        items: [
          'requirements/session/r023',
          'requirements/session/r024',
          'requirements/session/r025',
        ],
    },
    {
      type: 'category',
        label: 'Legal',
        items: [
          'requirements/legal/r331',
        ],
    },
    {
      type: 'category',
        label: 'Privacy',
        items: [
          'requirements/privacy/r189',
        ],
    },
  ],
  Agent: [
    'agent/introduction',
    'agent/installation',
  ],
  Findings: [
    'findings/introduction',
    {
      type: 'category',
        label: 'Security',
        items: [
          'findings/security/f001',
          'findings/security/f002',
          'findings/security/f003',
          'findings/security/f004',
          'findings/security/f005',
        ],
    },
    {
      type: 'category',
        label: 'Hygiene',
        items: [
          'findings/hygiene/f037',
        ],
    },
  ],
  Framework: {
    Framework: getDocs('framework'),
  },
  Dev: [
    'devs/products-repo-intro',
    {
      type: 'category',
      label: 'Stack',
      items: [
        {
          type: 'category',
          label: 'Git',
          items: [
            'devs/stack/git/commit-mr-guidelines',
          ]
        },
      ]
    },
    'devs/get-dev-keys',
    'devs/front-technologies',
    'devs/kubernetes-cluster-connect',
    'devs/dynamodb-patterns',
    'devs/graphql-api',
    'devs/mobile-technologies',
    'devs/writing-code-suggestions',
    'devs/analytics-conventions',
  ],
};
