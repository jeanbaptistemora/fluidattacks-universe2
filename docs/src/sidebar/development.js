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
    label: 'Writing Guidelines',
    items: [
      'development/writing/intro',
      {
        type: 'category',
        label: 'General Writing',
        items: [
          'development/writing/general/main',
          'development/writing/general/capital-letters',
        ]
      },
      'development/writing/documentation',
      'development/writing/blog-posts',
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
          'development/stack/aws/ebs',
          'development/stack/aws/ec2',
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
