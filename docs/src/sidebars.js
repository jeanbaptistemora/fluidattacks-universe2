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
          'criteria/privacy/r311',
        ],
    },
    {
      type: 'category',
        label: 'Data',
        items: [
          'criteria/data/r176',
        ],
    },
  ],
  Agent: [
    'agent/introduction',
    'agent/installation',
  ],
  Machine: [
    {
      type: 'category',
      label: 'Web',
      items: [
        'machine/web/asm',
        {
          type: 'category',
          label: 'Manage your organization',
          items: [
            'machine/web/organization/analytics-vulnerabilities',
            'machine/web/organization/analytics-generic',
          ],
        },
        {
          type: 'category',
          label: 'Manage your groups',
          items: [
            'machine/web/groups/vulnerabilities',
            'machine/web/groups/consulting',
            {
              type: 'category',
              label: 'Scope',
              items: [
                'machine/web/groups/scope/introduction',
                'machine/web/groups/scope/gitroots',
                'machine/web/groups/scope/files',
                'machine/web/groups/scope/portfolio',
              ],
            },
            'machine/web/groups/deleting-unsubscribing',
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
                'machine/web/vulnerabilities/management/reattacks',
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
            'machine/web/vulnerabilities/deleting-vulns',
          ],
        },
        'machine/web/glossary',
      ],
    },
    {
      type: 'category',
      label: 'Scanner',
      items: [
        'machine/scanner/benchmark',
        'machine/scanner/reproducibility',
        'machine/scanner/results',
      ],
    },
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
