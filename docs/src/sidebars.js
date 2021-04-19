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
          'criteria/data/r177',
          'criteria/data/r178',
        ],
    },
    {
      type: 'category',
        label: 'Source',
        items: [
          'criteria/source/r152',
          'criteria/source/r154',
          'criteria/source/r155',
        ],
    },
    {
      type: 'category',
        label: 'System',
        items: [
          'criteria/system/r186',
          'criteria/system/r273',
          'criteria/system/r280',
        ],
    },
    {
      type: 'category',
        label: 'Files',
        items: [
          'criteria/files/r036',
          'criteria/files/r037',
          'criteria/files/r039',
        ],
    },
    {
      type: 'category',
        label: 'Logs',
        items: [
          'criteria/logs/r075',
          'criteria/logs/r077',
          'criteria/logs/r078',
        ],
    },
    {
      type: 'category',
        label: 'Emails',
        items: [
          'criteria/emails/r115',
          'criteria/emails/r116',
          'criteria/emails/r117',
        ],
    },
    {
      type: 'category',
        label: 'Services',
        items: [
          'criteria/services/r262',
          'criteria/services/r265',
          'criteria/services/r330',
        ],
    },
    {
      type: 'category',
        label: 'Certificates',
        items: [
          'criteria/certificates/r088',
          'criteria/certificates/r089',
          'criteria/certificates/r090',
        ],
    },
    {
      type: 'category',
        label: 'Cryptography',
        items: [
          'criteria/cryptography/r145',
          'criteria/cryptography/r146',
          'criteria/cryptography/r147',
        ],
    },
    {
      type: 'category',
        label: 'Architecture',
        items: [
          'criteria/architecture/r048',
          'criteria/architecture/r050',
          'criteria/architecture/r051',
        ],
    },
    {
      type: 'category',
        label: 'Networks',
        items: [
          'criteria/networks/r247',
          'criteria/networks/r248',
        ],
    },
  ],
  Machine: [
    {
      type: 'category',
      label: 'App',
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
            'machine/web/groups/events',
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
        'machine/scanner/introduction',
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
  ],
  Squad: [
    'squad/introduction',
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
  Security: [
    'security/introduction',
    {
      type: 'category',
      label: 'Transparency',
      items: [
        'security/transparency/open-source',
        'security/transparency/public-indidents',
        'security/transparency/data-leakage-policy',
        'security/transparency/status-page',
      ],
    },
    {
      type: 'category',
      label: 'Confidentiality',
      items: [
        'security/confidentiality/encryption-rest',
        'security/confidentiality/encryption-transit',
        'security/confidentiality/hacking-our-technology',
        'security/confidentiality/personnel-nda',
        'security/confidentiality/hire-directly',
        'security/confidentiality/formatting-data',
      ],
    },
    {
      type: 'category',
      label: 'Authentication',
      items: [
        'security/authentication/clients',
        'security/authentication/internal',
      ],
    },
    {
      type: 'category',
      label: 'Authorization',
      items: [
        'security/authorization/clients',
        'security/authorization/internal',
        'security/authorization/secret-rotation',
        'security/authorization/access-revocation',
        'security/authorization/secure-mobile-policies',
      ],
    },
    {
      type: 'category',
      label: 'Privacy',
      items: [
        'security/privacy/project-pseudonymization',
        'security/privacy/email-obfuscation',
        'security/privacy/secure-data-delivery',
        'security/privacy/unsubscribe-email',
        'security/privacy/transparent-cookie-usage',
        'security/privacy/data-policies',
        'security/privacy/otr-messaging',
        'security/privacy/employee-time-tracking',
        'security/privacy/polygraph-tests',
      ],
    },
    {
      type: 'category',
      label: 'Non-repudiation',
      items: [
        'security/non-repudiation/everything-as-code',
        'security/non-repudiation/extensive-logs'
      ],
    },
    {
      type: 'category',
      label: 'Availability',
      items: [
        'security/availability/distributed-applications',
        'security/availability/distributed-firewall',
        'security/availability/forever-lasting-backups',
        'security/availability/everything-backed-up',
      ],
    },
    {
      type: 'category',
      label: 'Resilience',
      items: [
        'security/resilience/redundant-roles',
        'security/resilience/everything-decentralized',
        'security/resilience/equipment-telecommuting',
      ],
    },
    {
      type: 'category',
      label: 'Integrity',
      items: [
        'security/integrity/certified-hackers',
        'security/integrity/hiring-process',
        'security/integrity/secure-emails',
        'security/integrity/developing-integrity',
        'security/integrity/static-website',
      ],
    },
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
            'development/stack/git/commits',
            'development/stack/git/merge-requests',
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
