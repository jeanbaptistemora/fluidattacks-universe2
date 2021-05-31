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
  About: [
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
  ],
  Criteria: [
    'criteria/introduction',
    {
      type: 'category',
      label: 'Vulnerabilities',
      items: [
        'criteria/vulnerabilities/introduction',
        {
          type: 'category',
          label: 'Collect Information',
          items: [
            'criteria/vulnerabilities/f009',
            'criteria/vulnerabilities/f011',
            'criteria/vulnerabilities/f017',
            'criteria/vulnerabilities/f019',
            'criteria/vulnerabilities/f020',
            'criteria/vulnerabilities/f022',
            'criteria/vulnerabilities/f025',
            'criteria/vulnerabilities/f026',
            'criteria/vulnerabilities/f028',
            'criteria/vulnerabilities/f030',
            'criteria/vulnerabilities/f036',
            {
              type: 'category',
              label: 'Technical information leak',
              items: [
                'criteria/vulnerabilities/037/description',
                {
                  type: 'category',
                  label: 'Details',
                  items: [
                    'criteria/vulnerabilities/037/details/js-console',
                  ],
                },
              ],
            },
            'criteria/vulnerabilities/f038',
            'criteria/vulnerabilities/f040',
            'criteria/vulnerabilities/f046',
            'criteria/vulnerabilities/f047',
            {
              type: 'category',
              label: 'Insecure encryption algorithm',
              items: [
                'criteria/vulnerabilities/052/description',
                {
                  type: 'category',
                  label: 'Details',
                  items: [
                    'criteria/vulnerabilities/052/details/cipher-suites',
                    'criteria/vulnerabilities/052/details/ssl',
                  ],
                },
              ],
            },
            'criteria/vulnerabilities/f054',
            'criteria/vulnerabilities/f059',
            'criteria/vulnerabilities/f069',
            'criteria/vulnerabilities/f082',
            'criteria/vulnerabilities/f085',
            'criteria/vulnerabilities/f116',
            'criteria/vulnerabilities/f119',
          ],
        },
        {
          type: 'category',
          label: 'Inject Unexpected',
          items: [
          {
            type: 'category',
            label: 'SQL injection',
            items: [
              'criteria/vulnerabilities/001/description',
              {
                type: 'category',
                label: 'Details',
                items: [
                  'criteria/vulnerabilities/001/details/spring-data-java-persistence-api',
                ],
              },
            ],
          },
          'criteria/vulnerabilities/f004',
          'criteria/vulnerabilities/f008',
          'criteria/vulnerabilities/f010',
          'criteria/vulnerabilities/f021',
          'criteria/vulnerabilities/f045',
          'criteria/vulnerabilities/f063',
          'criteria/vulnerabilities/f083',
          'criteria/vulnerabilities/f090',
          'criteria/vulnerabilities/f096',
          'criteria/vulnerabilities/f105',
          'criteria/vulnerabilities/f106',
          'criteria/vulnerabilities/f107',
          ],
        },
        {
          type: 'category',
          label: 'Deceptive Interactions',
          items: [
            'criteria/vulnerabilities/f023',
            'criteria/vulnerabilities/f032',
            'criteria/vulnerabilities/f078',
            'criteria/vulnerabilities/f084',
            'criteria/vulnerabilities/f086',
            'criteria/vulnerabilities/f097',
            'criteria/vulnerabilities/f100',
            'criteria/vulnerabilities/f114',
          ],
        },
        {
          type: 'category',
          label: 'Abuse Functionality',
          items: [
            'criteria/vulnerabilities/f002',
            'criteria/vulnerabilities/f003',
            'criteria/vulnerabilities/f014',
            'criteria/vulnerabilities/f033',
            'criteria/vulnerabilities/f048',
            {
              type: 'category',
              label: 'Insecure service configuration',
              items: [
                'criteria/vulnerabilities/055/description',
                {
                  type: 'category',
                  label: 'Details',
                  items: [
                    'criteria/vulnerabilities/055/details/aws-ebs-encryption',
                    'criteria/vulnerabilities/055/details/aws-s3-server-side-encryption',
                  ],
                },
              ],
            },
            'criteria/vulnerabilities/f058',
            'criteria/vulnerabilities/f060',
            'criteria/vulnerabilities/f061',
            'criteria/vulnerabilities/f064',
            'criteria/vulnerabilities/f065',
            'criteria/vulnerabilities/f067',
            'criteria/vulnerabilities/f070',
            'criteria/vulnerabilities/f072',
            'criteria/vulnerabilities/f073',
            'criteria/vulnerabilities/f074',
            'criteria/vulnerabilities/f079',
            'criteria/vulnerabilities/f087',
            'criteria/vulnerabilities/f088',
            'criteria/vulnerabilities/f093',
            'criteria/vulnerabilities/f101',
            'criteria/vulnerabilities/f102',
            'criteria/vulnerabilities/f108',
            'criteria/vulnerabilities/f110',
            'criteria/vulnerabilities/f113',
            'criteria/vulnerabilities/f117',
            'criteria/vulnerabilities/f118',
            'criteria/vulnerabilities/f120',
          ],
        },
        {
          type: 'category',
          label: 'Probabilistic Techniques',
          items: [
            'criteria/vulnerabilities/f034',
            'criteria/vulnerabilities/f035',
            'criteria/vulnerabilities/f041',
            'criteria/vulnerabilities/f050',
            'criteria/vulnerabilities/f053',
          ],
        },
        {
          type: 'category',
          label: 'Subvert Access',
          items: [
            'criteria/vulnerabilities/f005',
            'criteria/vulnerabilities/f006',
            'criteria/vulnerabilities/f007',
            'criteria/vulnerabilities/f013',
            'criteria/vulnerabilities/f018',
            'criteria/vulnerabilities/f024',
            'criteria/vulnerabilities/f027',
            {
              type: 'category',
              label: 'Excessive privileges',
              items: [
                'criteria/vulnerabilities/031/description',
                {
                  type: 'category',
                  label: 'Details',
                  items: [
                    'criteria/vulnerabilities/031/details/aws-iam-pass-role',
                    'criteria/vulnerabilities/031/details/java-io-file-create-temp-file',
                  ],
                },
              ],
            },
            'criteria/vulnerabilities/f039',
            'criteria/vulnerabilities/f042',
            'criteria/vulnerabilities/f049',
            'criteria/vulnerabilities/f051',
            'criteria/vulnerabilities/f056',
            'criteria/vulnerabilities/f062',
            'criteria/vulnerabilities/f068',
            'criteria/vulnerabilities/f075',
            'criteria/vulnerabilities/f076',
            'criteria/vulnerabilities/f081',
            'criteria/vulnerabilities/f115',
            'criteria/vulnerabilities/f121',
          ],
        },
        {
          type: 'category',
          label: 'Manipulate Data',
          items: [
            'criteria/vulnerabilities/f098',
            'criteria/vulnerabilities/f103',
            'criteria/vulnerabilities/f111',
          ],
        },
        {
          type: 'category',
          label: 'Manipulate System',
          items: [
            'criteria/vulnerabilities/f029',
            'criteria/vulnerabilities/f077',
            'criteria/vulnerabilities/f091',
            'criteria/vulnerabilities/f104',
          ],
        },
        {
          type: 'category',
          label: 'Protocol Manipulation',
          items: [
            'criteria/vulnerabilities/f015',
            {
              type: 'category',
              label: 'Improperly set HTTP headers',
              items: [
                'criteria/vulnerabilities/043/description',
                {
                  type: 'category',
                  label: 'Details',
                  items: [
                    'criteria/vulnerabilities/043/details/strict-transport-security',
                  ],
                },
              ],
            },
            'criteria/vulnerabilities/f044',
          ],
        },
      ],
    },
    {
      type: 'category',
      label: 'Requirements',
      items: [
        'criteria/requirements/introduction',
        {
          type: 'category',
          label: 'Credentials',
          items: [
            'criteria/requirements/credentials/r126',
            'criteria/requirements/credentials/r127',
            'criteria/requirements/credentials/r128',
            'criteria/requirements/credentials/r129',
            'criteria/requirements/credentials/r130',
            'criteria/requirements/credentials/r131',
            'criteria/requirements/credentials/r132',
            'criteria/requirements/credentials/r133',
            'criteria/requirements/credentials/r134',
            'criteria/requirements/credentials/r135',
            'criteria/requirements/credentials/r136',
            'criteria/requirements/credentials/r137',
            'criteria/requirements/credentials/r138',
            'criteria/requirements/credentials/r139',
            'criteria/requirements/credentials/r140',
            'criteria/requirements/credentials/r141',
            'criteria/requirements/credentials/r142',
            'criteria/requirements/credentials/r143',
            'criteria/requirements/credentials/r144',
            'criteria/requirements/credentials/r332',
            'criteria/requirements/credentials/r333',
            'criteria/requirements/credentials/r347',
            'criteria/requirements/credentials/r358',
            'criteria/requirements/credentials/r367',
            'criteria/requirements/credentials/r380',
          ],
        },
        {
          type: 'category',
          label: 'Authentication',
          items: [
            'criteria/requirements/authentication/r122',
            'criteria/requirements/authentication/r153',
            'criteria/requirements/authentication/r225',
            'criteria/requirements/authentication/r226',
            'criteria/requirements/authentication/r227',
            'criteria/requirements/authentication/r228',
            'criteria/requirements/authentication/r229',
            'criteria/requirements/authentication/r231',
            'criteria/requirements/authentication/r232',
            'criteria/requirements/authentication/r235',
            'criteria/requirements/authentication/r236',
            'criteria/requirements/authentication/r237',
            'criteria/requirements/authentication/r238',
            'criteria/requirements/authentication/r264',
            'criteria/requirements/authentication/r319',
            'criteria/requirements/authentication/r328',
            'criteria/requirements/authentication/r334',
            'criteria/requirements/authentication/r335',
            'criteria/requirements/authentication/r362',
            'criteria/requirements/authentication/r368',
          ],
        },
        {
          type: 'category',
          label: 'Authorization',
          items: [
            'criteria/requirements/authorization/r033',
            'criteria/requirements/authorization/r034',
            'criteria/requirements/authorization/r035',
            'criteria/requirements/authorization/r095',
            'criteria/requirements/authorization/r096',
            'criteria/requirements/authorization/r114',
            'criteria/requirements/authorization/r341',
          ],
        },
        {
          type: 'category',
          label: 'Session',
          items: [
            'criteria/requirements/session/r023',
            'criteria/requirements/session/r024',
            'criteria/requirements/session/r025',
            'criteria/requirements/session/r026',
            'criteria/requirements/session/r027',
            'criteria/requirements/session/r028',
            'criteria/requirements/session/r029',
            'criteria/requirements/session/r030',
            'criteria/requirements/session/r031',
            'criteria/requirements/session/r032',
            'criteria/requirements/session/r357',
            'criteria/requirements/session/r369',
          ],
        },
        {
          type: 'category',
          label: 'Legal',
          items: [
            'criteria/requirements/legal/r331',
          ],
        },
        {
          type: 'category',
          label: 'Privacy',
          items: [
            'criteria/requirements/privacy/r189',
            'criteria/requirements/privacy/r310',
            'criteria/requirements/privacy/r311',
            'criteria/requirements/privacy/r312',
            'criteria/requirements/privacy/r313',
            'criteria/requirements/privacy/r314',
            'criteria/requirements/privacy/r315',
            'criteria/requirements/privacy/r316',
            'criteria/requirements/privacy/r317',
            'criteria/requirements/privacy/r318',
            'criteria/requirements/privacy/r343',
            'criteria/requirements/privacy/r360',
          ],
        },
        {
          type: 'category',
          label: 'Data',
          items: [
            'criteria/requirements/data/r176',
            'criteria/requirements/data/r177',
            'criteria/requirements/data/r178',
            'criteria/requirements/data/r180',
            'criteria/requirements/data/r181',
            'criteria/requirements/data/r183',
            'criteria/requirements/data/r184',
            'criteria/requirements/data/r185',
            'criteria/requirements/data/r300',
            'criteria/requirements/data/r301',
            'criteria/requirements/data/r305',
            'criteria/requirements/data/r321',
            'criteria/requirements/data/r329',
            'criteria/requirements/data/r365',
            'criteria/requirements/data/r375',
          ],
        },
        {
          type: 'category',
          label: 'Source',
          items: [
            'criteria/requirements/source/r152',
            'criteria/requirements/source/r154',
            'criteria/requirements/source/r155',
            'criteria/requirements/source/r156',
            'criteria/requirements/source/r157',
            'criteria/requirements/source/r158',
            'criteria/requirements/source/r159',
            'criteria/requirements/source/r160',
            'criteria/requirements/source/r161',
            'criteria/requirements/source/r162',
            'criteria/requirements/source/r164',
            'criteria/requirements/source/r167',
            'criteria/requirements/source/r168',
            'criteria/requirements/source/r169',
            'criteria/requirements/source/r171',
            'criteria/requirements/source/r172',
            'criteria/requirements/source/r173',
            'criteria/requirements/source/r174',
            'criteria/requirements/source/r175',
            'criteria/requirements/source/r302',
            'criteria/requirements/source/r323',
            'criteria/requirements/source/r337',
            'criteria/requirements/source/r342',
            'criteria/requirements/source/r344',
            'criteria/requirements/source/r345',
            'criteria/requirements/source/r359',
            'criteria/requirements/source/r366',
            'criteria/requirements/source/r379',
            'criteria/requirements/source/r381',
          ],
        },
        {
          type: 'category',
          label: 'System',
          items: [
            'criteria/requirements/system/r186',
            'criteria/requirements/system/r273',
            'criteria/requirements/system/r280',
            'criteria/requirements/system/r284',
            'criteria/requirements/system/r363',
            'criteria/requirements/system/r374',
          ],
        },
        {
          type: 'category',
          label: 'Files',
          items: [
            'criteria/requirements/files/r036',
            'criteria/requirements/files/r037',
            'criteria/requirements/files/r039',
            'criteria/requirements/files/r040',
            'criteria/requirements/files/r041',
            'criteria/requirements/files/r042',
            'criteria/requirements/files/r043',
            'criteria/requirements/files/r044',
            'criteria/requirements/files/r045',
            'criteria/requirements/files/r046',
            'criteria/requirements/files/r339',
            'criteria/requirements/files/r340',
          ],
        },
        {
          type: 'category',
          label: 'Logs',
          items: [
            'criteria/requirements/logs/r075',
            'criteria/requirements/logs/r077',
            'criteria/requirements/logs/r078',
            'criteria/requirements/logs/r079',
            'criteria/requirements/logs/r080',
            'criteria/requirements/logs/r083',
            'criteria/requirements/logs/r084',
            'criteria/requirements/logs/r085',
            'criteria/requirements/logs/r322',
            'criteria/requirements/logs/r376',
            'criteria/requirements/logs/r377',
            'criteria/requirements/logs/r378',
          ],
        },
        {
          type: 'category',
          label: 'Emails',
          items: [
            'criteria/requirements/emails/r115',
            'criteria/requirements/emails/r116',
            'criteria/requirements/emails/r117',
            'criteria/requirements/emails/r118',
            'criteria/requirements/emails/r119',
            'criteria/requirements/emails/r121',
            'criteria/requirements/emails/r123',
          ],
        },
        {
          type: 'category',
          label: 'Services',
          items: [
            'criteria/requirements/services/r262',
            'criteria/requirements/services/r265',
            'criteria/requirements/services/r330',
          ],
        },
        {
          type: 'category',
          label: 'Certificates',
          items: [
            'criteria/requirements/certificates/r088',
            'criteria/requirements/certificates/r089',
            'criteria/requirements/certificates/r090',
            'criteria/requirements/certificates/r091',
            'criteria/requirements/certificates/r092',
            'criteria/requirements/certificates/r093',
            'criteria/requirements/certificates/r364',
            'criteria/requirements/certificates/r373',
          ],
        },
        {
          type: 'category',
          label: 'Cryptography',
          items: [
            'criteria/requirements/cryptography/r145',
            'criteria/requirements/cryptography/r146',
            'criteria/requirements/cryptography/r147',
            'criteria/requirements/cryptography/r148',
            'criteria/requirements/cryptography/r149',
            'criteria/requirements/cryptography/r150',
            'criteria/requirements/cryptography/r151',
            'criteria/requirements/cryptography/r223',
            'criteria/requirements/cryptography/r224',
            'criteria/requirements/cryptography/r336',
            'criteria/requirements/cryptography/r338',
            'criteria/requirements/cryptography/r346',
            'criteria/requirements/cryptography/r351',
            'criteria/requirements/cryptography/r361',
            'criteria/requirements/cryptography/r370',
            'criteria/requirements/cryptography/r371',
            'criteria/requirements/cryptography/r372',
          ],
        },
        {
          type: 'category',
          label: 'Architecture',
          items: [
            'criteria/requirements/architecture/r048',
            'criteria/requirements/architecture/r050',
            'criteria/requirements/architecture/r051',
            'criteria/requirements/architecture/r062',
            'criteria/requirements/architecture/r072',
            'criteria/requirements/architecture/r266',
            'criteria/requirements/architecture/r320',
            'criteria/requirements/architecture/r324',
            'criteria/requirements/architecture/r325',
            'criteria/requirements/architecture/r327',
            'criteria/requirements/architecture/r348',
            'criteria/requirements/architecture/r349',
            'criteria/requirements/architecture/r355',
          ],
        },
        {
          type: 'category',
          label: 'Networks',
          items: [
            'criteria/requirements/networks/r247',
            'criteria/requirements/networks/r248',
            'criteria/requirements/networks/r249',
            'criteria/requirements/networks/r250',
            'criteria/requirements/networks/r251',
            'criteria/requirements/networks/r252',
            'criteria/requirements/networks/r253',
            'criteria/requirements/networks/r254',
            'criteria/requirements/networks/r255',
            'criteria/requirements/networks/r257',
            'criteria/requirements/networks/r258',
            'criteria/requirements/networks/r259',
            'criteria/requirements/networks/r356',
          ],
        },
        {
          type: 'category',
          label: 'Virtualization',
          items: [
            'criteria/requirements/virtualization/r221',
            'criteria/requirements/virtualization/r222',
          ],
        },
        {
          type: 'category',
          label: 'Devices',
          items: [
            'criteria/requirements/devices/r205',
            'criteria/requirements/devices/r206',
            'criteria/requirements/devices/r209',
            'criteria/requirements/devices/r210',
            'criteria/requirements/devices/r213',
            'criteria/requirements/devices/r214',
            'criteria/requirements/devices/r326',
            'criteria/requirements/devices/r350',
            'criteria/requirements/devices/r352',
            'criteria/requirements/devices/r353',
            'criteria/requirements/devices/r354',
          ],
        },
        {
          type: 'category',
          label: 'Social',
          items: [
            'criteria/requirements/social/r260',
            'criteria/requirements/social/r261',
          ],
        },
      ],
    },
    {
      type: 'category',
      label: 'Compliance',
      items: [
        'criteria/compliance/introduction',
        'criteria/compliance/pcidss',
        'criteria/compliance/owaspasvs',
        'criteria/compliance/bsimm',
        'criteria/compliance/capec',
        'criteria/compliance/cwe',
        'criteria/compliance/eprivacy',
        'criteria/compliance/gdpr',
        'criteria/compliance/hipaa',
        'criteria/compliance/iso',
        'criteria/compliance/nerc',
        'criteria/compliance/nist',
        'criteria/compliance/owaspten',
      ],
    },
  ],
  Machine: [
    {
      type: 'category',
      label: 'App',
      items: [
        'machine/app/asm',
        {
          type: 'category',
          label: 'Organizations',
          items: [
            'machine/app/organization/analytics-vulnerabilities',
            'machine/app/organization/analytics-generic',
          ],
        },
        {
          type: 'category',
          label: 'Groups',
          items: [
            'machine/app/groups/vulnerabilities',
            'machine/app/groups/events',
            {
              type: 'category',
              label: 'Scope',
              items: [
                'machine/app/groups/scope/introduction',
                'machine/app/groups/scope/gitroots',
                'machine/app/groups/scope/exclusions',
                'machine/app/groups/scope/files',
                'machine/app/groups/scope/portfolio',
              ],
            },
            'machine/app/groups/delete',
            'machine/app/groups/unsubscribe',          ],
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
            'machine/app/vulnerabilities/deleting-vulns',
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
  ],
  Squad: [
    'squad/reattacks',
    'squad/consulting',
  ],
  Framework: {
    Framework: getDocs('framework'),
  },
  Development: [
    'development/products-repo-intro',
    {
      type: 'category',
      label: 'Contributing',
      items: [
        'development/contributing/introduction',
        'development/contributing/dependencies',
        'development/contributing/editor',
        'development/contributing/environment',
      ]
    },
    {
      type: 'category',
      label: 'Stack',
      items: [
        'development/stack/introduction',
        'development/stack/cloudflare',
        {
          type: 'category',
          label: 'Git',
          items: [
            'development/stack/git/commits',
            'development/stack/git/merge-requests',
          ]
        },
        'development/stack/gitlab-ci',
        'development/stack/kubernetes',
        'development/stack/okta',
        'development/stack/sops',
        'development/stack/terraform',
      ]
    },
    'development/get-dev-keys',
    'development/front-technologies',
    'development/dynamodb-patterns',
    'development/graphql-api',
    'development/mobile-technologies',
    'development/writing-code-suggestions',
    'development/analytics-conventions',
  ],
};
