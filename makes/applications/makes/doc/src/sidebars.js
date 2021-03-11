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
      label: 'Groups',
      items: [
        'web/groups/vulnerabilities',
        'web/groups/devsecops',
        'web/groups/events',
        'web/groups/consulting',
        'web/groups/authors',
        'web/groups/scope',
      ],
    },
    {
      type: 'category',
      label: 'Vulnerabilities',
      items: [
        'web/vulnerabilities/vulnsmanagement',
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
