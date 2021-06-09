const { ABOUT } = require('./about.js')
const { CRITERIA } = require('./criteria.js')
const { MACHINE } = require('./machine.js')
const { DEVELOPMENT } = require('./development.js')

module.exports = {
  About: ABOUT,
  Criteria: CRITERIA,
  Machine: MACHINE,
  Squad: [
    'squad/reattacks',
    'squad/consulting',
  ],
  Development: DEVELOPMENT,
  Writing: [
    'writing/intro',
    {
      type: 'category',
      label: 'General Writing Tips',
      items: [
        'writing/general/main',
        'writing/general/capital-letters',
      ]
    },
    'writing/documentation',
  ],
};
