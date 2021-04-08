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
  Rules: [
    'rules/intro',
    {
      type: 'category',
      label: 'Credentials',
      items: [
        'rules/credentials/r126',
        'rules/credentials/r127',
        'rules/credentials/r128',
        'rules/credentials/r129',
        'rules/credentials/r130',
        'rules/credentials/r131',
        'rules/credentials/r132',
        'rules/credentials/r133',
        'rules/credentials/r134',
        'rules/credentials/r135',
        'rules/credentials/r136',
        'rules/credentials/r137',
        'rules/credentials/r138',
        'rules/credentials/r139',
        'rules/credentials/r140',
        'rules/credentials/r141',
        'rules/credentials/r142',
        'rules/credentials/r143',
        'rules/credentials/r144',
        'rules/credentials/r332',
        'rules/credentials/r333',
      ],
    },
    {
      type: 'category',
      label: 'Authentication',
      items: [
        'rules/authentication/r122',
        'rules/authentication/r153',
        'rules/authentication/r225',
      ],
    },
    {
    type: 'category',
      label: 'Authorization',
      items: [
        'rules/authorization/r033',
        'rules/authorization/r034',
        'rules/authorization/r035',
      ],
    },
    {
      type: 'category',
        label: 'Session',
        items: [
          'rules/session/r023',
          'rules/session/r024',
        ],
    },
  ],
  Agent: [
    'agent/introduction',
    'agent/installation',
  ],
  Framework: {
    Framework: getDocs('framework'),
  },
  Devs: [
    'devs/commit-mr-guidelines',
    {
      type: 'category',
      label: 'Integrates',
      items: [
        'devs/integrates/get-dev-keys',
        'devs/integrates/integrates-front',
        'devs/integrates/kubernetes-cluster-connect',
        'devs/integrates/dynamodb-patterns',
        'devs/integrates/graphql-api',
        'devs/integrates/integrates-mobile',
        'devs/integrates/writing-code-suggestions',
      ]
    },
    {
      type: 'category',
      label: 'Observes',
      items: [
        'devs/observes/observes-conventions',
      ]
    },
  ],
};
