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
    'squad/false-negatives',
  ],
  Development: DEVELOPMENT,
};
