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
    'web/organization',
    {
      type: 'category',
      label: 'Manage your groups',
      items: [
        'web/groups/vulnerabilities',
        'web/groups/devsecops',
        'web/groups/events',
        'web/groups/consulting',
        'web/groups/authors',
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
        'web/vulnerabilities/description',
        'web/vulnerabilities/severity',
      ],
    },
    'web/glossary',
  ],
  Mobile: {
    Mobile: getDocs('mobile'),
  },
  API: {
    API: getDocs('api'),
  },
  Agent: {
    Agent: getDocs('agent'),
  },
  Framework: {
    Framework: getDocs('framework'),
  },
};
