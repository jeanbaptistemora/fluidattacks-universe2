const About = [
  {
    type: 'category',
    label: 'FAQ',
    items: [
      'about/faq/general',
      'about/faq/machine',
      'about/faq/estimation',
      'about/faq/requirements',
      'about/faq/billing',
      'about/faq/speed',
      'about/faq/vulnerabilities',
      'about/faq/others',
    ],
  },
  {
    type: 'category',
    label: 'SLA',
    items: [
      'about/sla/introduction',
      'about/sla/availability',
      'about/sla/accuracy',
      'about/sla/response',
    ],
  },
  {
    type: 'category',
    label: 'Security',
    items: [
      'about/security/introduction',
      {
        type: 'category',
        label: 'Transparency',
        items: [
          'about/security/transparency/information-security-responsibility',
          'about/security/transparency/open-source',
          'about/security/transparency/public-incidents',
          'about/security/transparency/data-leakage-policy',
          'about/security/transparency/help-channel',
          'about/security/transparency/status-page',
        ],
      },
      {
        type: 'category',
        label: 'Confidentiality',
        items: [
          'about/security/confidentiality/encryption-rest',
          'about/security/confidentiality/encryption-transit',
          'about/security/confidentiality/hacking-our-technology',
          'about/security/confidentiality/personnel-nda',
          'about/security/confidentiality/hire-directly',
          'about/security/confidentiality/formatting-data',
        ],
      },
      {
        type: 'category',
        label: 'Authentication',
        items: [
          'about/security/authentication/clients',
          'about/security/authentication/internal',
        ],
      },
      {
        type: 'category',
        label: 'Authorization',
        items: [
          'about/security/authorization/clients',
          'about/security/authorization/internal',
          'about/security/authorization/secret-rotation',
          'about/security/authorization/access-revocation',
          'about/security/authorization/secure-mobile-policies',
        ],
      },
      {
        type: 'category',
        label: 'Privacy',
        items: [
          'about/security/privacy/project-pseudonymization',
          'about/security/privacy/email-obfuscation',
          'about/security/privacy/secure-data-delivery',
          'about/security/privacy/unsubscribe-email',
          'about/security/privacy/transparent-use-cookies',
          'about/security/privacy/data-policies',
          'about/security/privacy/otr-messaging',
          'about/security/privacy/employee-time-tracking',
          'about/security/privacy/polygraph-tests',
        ],
      },
      {
        type: 'category',
        label: 'Non-repudiation',
        items: [
          'about/security/non-repudiation/everything-as-code',
          'about/security/non-repudiation/extensive-logs'
        ],
      },
      {
        type: 'category',
        label: 'Availability',
        items: [
          'about/security/availability/distributed-applications',
          'about/security/availability/distributed-firewall',
          'about/security/availability/everything-backed-up',
          'about/security/availability/recovery-objective',
          'about/security/availability/multiple-zones',
        ],
      },
      {
        type: 'category',
        label: 'Resilience',
        items: [
          'about/security/resilience/redundant-roles',
          'about/security/resilience/everything-decentralized',
          'about/security/resilience/equipment-telecommuting',
        ],
      },
      {
        type: 'category',
        label: 'Integrity',
        items: [
          'about/security/integrity/certified-cloud-provider',
          'about/security/integrity/certified-hackers',
          'about/security/integrity/hiring-process',
          'about/security/integrity/secure-emails',
          'about/security/integrity/developing-integrity',
          'about/security/integrity/static-website',
        ],
      },
    ],
  },
  'about/glossary',
]

const Criteria = [
  'criteria/introduction',
  {
    type: 'category',
    label: 'Compliance',
    items: [
      {
        type: 'autogenerated',
        dirName: 'criteria/Compliance',
      },
    ],
  },
  {
    type: 'category',
    label: 'Requirements',
    items: [
      'criteria/Requirements/introduction',
      {
        type: 'category',
        label: 'Credentials',
        items: [
          {
            type: 'autogenerated',
            dirName: 'criteria/Requirements/Credentials',
          },
        ]
      },
      {
        type: 'category',
        label: 'Authentication',
        items: [
          {
            type: 'autogenerated',
            dirName: 'criteria/Requirements/Authentication',
          },
        ],
      },
      {
        type: 'category',
        label: 'Authorization',
        items: [
          {
            type: 'autogenerated',
            dirName: 'criteria/Requirements/Authorization',
          },
        ],
      },
      {
        type: 'category',
        label: 'Session',
        items: [
          {
            type: 'autogenerated',
            dirName: 'criteria/Requirements/Session',
          },
        ],
      },
      {
        type: 'category',
        label: 'Legal',
        items: [
          {
            type: 'autogenerated',
            dirName: 'criteria/Requirements/Legal',
          },
        ],
      },
      {
        type: 'category',
        label: 'Privacy',
        items: [
          {
            type: 'autogenerated',
            dirName: 'criteria/Requirements/Privacy',
          },
        ],
      },
      {
        type: 'category',
        label: 'Data',
        items: [
          {
            type: 'autogenerated',
            dirName: 'criteria/Requirements/Data',
          },
        ],
      },
      {
        type: 'category',
        label: 'Source',
        items: [
          {
            type: 'autogenerated',
            dirName: 'criteria/Requirements/Source',
          },
        ],
      },
      {
        type: 'category',
        label: 'System',
        items: [
          {
            type: 'autogenerated',
            dirName: 'criteria/Requirements/System',
          },
        ],
      },
      {
        type: 'category',
        label: 'Files',
        items: [
          {
            type: 'autogenerated',
            dirName: 'criteria/Requirements/Files',
          },
        ],
      },
      {
        type: 'category',
        label: 'Logs',
        items: [
          {
            type: 'autogenerated',
            dirName: 'criteria/Requirements/Logs',
          },
        ],
      },
      {
        type: 'category',
        label: 'Emails',
        items: [
          {
            type: 'autogenerated',
            dirName: 'criteria/Requirements/Emails',
          },
        ],
      },
      {
        type: 'category',
        label: 'Services',
        items: [
          {
            type: 'autogenerated',
            dirName: 'criteria/Requirements/Services',
          },
        ],
      },
      {
        type: 'category',
        label: 'Certificates',
        items: [
          {
            type: 'autogenerated',
            dirName: 'criteria/Requirements/Certificates',
          },
        ],
      },
      {
        type: 'category',
        label: 'Cryptography',
        items: [
          {
            type: 'autogenerated',
            dirName: 'criteria/Requirements/Cryptography',
          },
        ],
      },
      {
        type: 'category',
        label: 'Architecture',
        items: [
          {
            type: 'autogenerated',
            dirName: 'criteria/Requirements/Architecture',
          },
        ],
      },
      {
        type: 'category',
        label: 'Networks',
        items: [
          {
            type: 'autogenerated',
            dirName: 'criteria/Requirements/Networks',
          },
        ],
      },
      {
        type: 'category',
        label: 'Virtualization',
        items: [
          {
            type: 'autogenerated',
            dirName: 'criteria/Requirements/Virtualization',
          },
        ],
      },
      {
        type: 'category',
        label: 'Devices',
        items: [
          {
            type: 'autogenerated',
            dirName: 'criteria/Requirements/Devices',
          },
        ],
      },
      {
        type: 'category',
        label: 'Social',
        items: [
          {
            type: 'autogenerated',
            dirName: 'criteria/Requirements/Social',
          },
        ],
      },
    ],
  },
  {
    type: 'category',
    label: 'Vulnerabilities',
    items: [
      {
        type: 'autogenerated',
        dirName: 'criteria/Vulnerabilities',
      },
    ],
  },
]

const Development = [
  'development/products-repo-intro',
  {
    type: 'category',
    label: 'Setup',
    items: [
      'development/setup/introduction',
      'development/setup/dependencies',
      'development/setup/editor',
      'development/setup/environment',
    ]
  },
  {
    type: 'category',
    label: 'Writing',
    items: [
      'development/writing/intro',
      {
        type: 'category',
        label: 'General',
        items: [
          'development/writing/general/main',
          'development/writing/general/capital-letters',
          'development/writing/general/quotation-marks',
          'development/writing/general/italics',
          'development/writing/general/bold',
          'development/writing/general/numbers',
          'development/writing/general/others',
          'development/writing/general/lists',
          'development/writing/general/links',
        ]
      },
      {
        type: 'category',
        label: 'Blog',
        items: [
          'development/writing/blog/main',
          'development/writing/blog/code',
          'development/writing/blog/metadata',
          'development/writing/blog/submissions',
        ]
      },
      {
        type: 'category',
        label: 'Documentation',
        items: [
          'development/writing/documentation/main',
          'development/writing/documentation/metadata',
          'development/writing/documentation/markdown',
        ]
      },
      'development/writing/slb',
    ]
  },
  {
    type: 'category',
    label: 'Stack',
    items: [
      'development/stack/introduction',
      {
        type: 'category',
        label: 'AWS',
        items: [
          'development/stack/aws/introduction',
          'development/stack/aws/batch',
          'development/stack/aws/cloudwatch',
          'development/stack/aws/cost-management',
          'development/stack/aws/dynamodb',
          'development/stack/aws/ebs',
          'development/stack/aws/ec2',
          'development/stack/aws/eks',
          'development/stack/aws/elb',
          'development/stack/aws/iam',
          'development/stack/aws/kms',
          'development/stack/aws/lambda',
          'development/stack/aws/redis',
          'development/stack/aws/redshift',
          'development/stack/aws/s3',
          'development/stack/aws/sagemaker',
          'development/stack/aws/vpc',
          'development/stack/aws/vpn',
        ]
      },
      'development/stack/cloudflare',
      {
        type: 'category',
        label: 'Commitlint',
        items: [
          'development/stack/commitlint/introduction',
          {
            type: 'category',
            label: 'Syntax',
            items: [
              'development/stack/commitlint/syntax/commit',
              'development/stack/commitlint/syntax/merge-request',
            ]
          },
        ]
      },
      'development/stack/gitlab',
      'development/stack/gitlab-ci',
      'development/stack/kubernetes',
      'development/stack/okta',
      'development/stack/sops',
      'development/stack/terraform',
      'development/stack/ubiquiti',
    ]
  },
  'development/front-technologies',
  'development/dynamodb-patterns',
  'development/graphql-api',
  'development/writing-code-suggestions',
  'development/analytics-conventions',
  'development/melts',
]

const Machine = [
  {
    type: 'category',
    label: 'Web',
    items: [
      'machine/web/asm',
      'machine/web/self-enrollment',
      'machine/web/creating-organization',
      'machine/web/user-information',
      'machine/web/notifications',
      {
        type: 'category',
        label: 'Support',
        items: [
          'machine/web/support/live-chat',
        ],
      },
      {
        type: 'category',
        label: 'News',
        items: [
          'machine/web/news/subscription',
        ],
      },
      {
        type: 'category',
        label: 'Organizations',
        items: [
          'machine/web/organization/policies',
        ],
      },
      {
        type: 'category',
        label: 'Groups',
        items: [
          'machine/web/groups/introduction',
          'machine/web/groups/general',
          'machine/web/groups/vulnerabilities',
          'machine/web/groups/reports',
          'machine/web/groups/events',
          'machine/web/groups/stakeholders',
          'machine/web/groups/roles',
          'machine/web/groups/authors',
          'machine/web/groups/surface',
          {
            type: 'category',
            label: 'Scope',
            items: [
              'machine/web/groups/scope/introduction',
              'machine/web/groups/scope/roots',
              'machine/web/groups/scope/global-credentials',
              'machine/web/groups/scope/exclusions',
              'machine/web/groups/scope/files',
              'machine/web/groups/scope/portfolios',
            ],
          },
          'machine/web/groups/delete',
          'machine/web/groups/context',
          'machine/web/groups/agent',
          'machine/web/groups/services',
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
              'machine/web/vulnerabilities/management/general',
              'machine/web/vulnerabilities/management/vulnerability-description',
              'machine/web/vulnerabilities/management/to-do-list',
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
      {
        type: 'category',
        label: 'Analytics',
        items: [
          'machine/web/analytics/introduction',
          'machine/web/analytics/reports',
          'machine/web/analytics/common',
          'machine/web/analytics/organization',
          'machine/web/analytics/portfolio',
          'machine/web/analytics/groups',
          'machine/web/analytics/chart-options',
        ],
      },
      'machine/web/portfolios',
      'machine/web/stakeholders',
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

const Squad = [
  'squad/reattacks',
  'squad/consulting',
  {
    type: 'category',
    label: 'Support',
    items: [
      'squad/support/talk-expert',
    ],
  },
  'squad/false-negatives',
  'squad/weapons',
  'squad/counting-authors',
]

module.exports = {
  About: About,
  Criteria: Criteria,
  Machine: Machine,
  Squad: Squad,
  Development: Development,
};
