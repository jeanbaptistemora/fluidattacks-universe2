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
    'criteria/intro',
    {
      type: 'category',
      label: 'Credentials',
      items: [
        'criteria/credentials/r126',
        'criteria/credentials/r127',
        'criteria/credentials/r128',
        'criteria/credentials/r129',
        'criteria/credentials/r130',
        'criteria/credentials/r131',
        'criteria/credentials/r132',
        'criteria/credentials/r133',
        'criteria/credentials/r134',
        'criteria/credentials/r135',
        'criteria/credentials/r136',
        'criteria/credentials/r137',
        'criteria/credentials/r138',
        'criteria/credentials/r139',
        'criteria/credentials/r140',
        'criteria/credentials/r141',
        'criteria/credentials/r142',
        'criteria/credentials/r143',
        'criteria/credentials/r144',
        'criteria/credentials/r332',
        'criteria/credentials/r333',
      ],
    },
    {
      type: 'category',
      label: 'Authentication',
      items: [
        'criteria/authentication/r122',
        'criteria/authentication/r153',
        'criteria/authentication/r225',
      ],
    },
    {
    type: 'category',
      label: 'Authorization',
      items: [
        'criteria/authorization/r033',
        'criteria/authorization/r034',
        'criteria/authorization/r035',
      ],
    },
    {
      type: 'category',
        label: 'Session',
        items: [
          'criteria/session/r023',
          'criteria/session/r024',
          'criteria/session/r025',
        ],
    },
    {
      type: 'category',
        label: 'Legal',
        items: [
          'criteria/legal/r331',
        ],
    },
    {
      type: 'category',
        label: 'Privacy',
        items: [
          'criteria/privacy/r189',
          'criteria/privacy/r310',
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
    'owasp-benchmark/transparency',
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
