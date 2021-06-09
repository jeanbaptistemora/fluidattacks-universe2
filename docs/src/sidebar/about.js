const ABOUT = [
  {
    type: 'category',
    label: 'FAQ',
    items: [
      'about/faq/general',
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
          'about/security/transparency/open-source',
          'about/security/transparency/public-indidents',
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
          'about/security/privacy/transparent-cookie-usage',
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

module.exports = { ABOUT };
