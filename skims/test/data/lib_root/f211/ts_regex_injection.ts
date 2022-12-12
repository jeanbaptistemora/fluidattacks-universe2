const escapeStringRegexp = require('escape-string-regexp');
const safe = require('safe-regex');

function vuln_two(req, res) {
  const pattern1 = RegExp(req.query.pattern); // Noncompliant
  pattern1.test(req.query.input);
}


function vuln_one(req, res) {
  if(safe(req.query.pattern)) {
    const regex = RegExp(req.query.pattern); // Noncompliant
    regex.test(req.query.input);
  }
}


function secure(req, res) {
  const pattern = RegExp(escapeStringRegexp(req.query.pattern)); // Compliant
  pattern.test(req.query.input);
}
