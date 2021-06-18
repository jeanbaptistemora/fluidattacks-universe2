const DEVELOPMENT = [
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
          'development/writing/blog/metadata',
          'development/writing/blog/additional',
          'development/writing/blog/asciidoc',
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
          'development/stack/aws/cloudwatch',
          'development/stack/aws/ebs',
          'development/stack/aws/ec2',
          'development/stack/aws/eks',
          'development/stack/aws/iam',
          'development/stack/aws/kms',
          'development/stack/aws/s3',
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
    ]
  },
  'development/front-technologies',
  'development/dynamodb-patterns',
  'development/graphql-api',
  'development/mobile-technologies',
  'development/writing-code-suggestions',
  'development/analytics-conventions',
]

module.exports = { DEVELOPMENT };
