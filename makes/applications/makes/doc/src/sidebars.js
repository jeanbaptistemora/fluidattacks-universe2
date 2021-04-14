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
        'web/vulnerabilities/deleting-vulns',
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
  Criteria: [
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
  OwaspBenchmark: [
    'owasp-benchmark/introduction',
    'owasp-benchmark/our-score',
  ],
  Types: [
    'types/introduction',
    'types/f001',
    'types/f002',
    'types/f003',
    'types/f004',
    'types/f005',
    'types/f006',
    'types/f007',
    'types/f008',
    'types/f009',
    'types/f037',
  ],
  Framework: {
    Framework: getDocs('framework'),
  },
  Development: [
    'development/products-repo-intro',
    {
      type: 'category',
      label: 'Stack',
      items: [
        {
          type: 'category',
          label: 'Git',
          items: [
            'development/stack/git/commit-mr-guidelines',
          ]
        },
      ]
    },
    'development/get-dev-keys',
    'development/front-technologies',
    'development/kubernetes-cluster-connect',
    'development/dynamodb-patterns',
    'development/graphql-api',
    'development/mobile-technologies',
    'development/writing-code-suggestions',
    'development/analytics-conventions',
  ],
};
