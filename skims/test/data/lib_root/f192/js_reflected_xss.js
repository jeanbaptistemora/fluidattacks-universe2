import sanitizeHtml from "sanitize-html";

function vuln(req, res) {
  const tainted = req.query.name;

  res.send(tainted); // Noncompliant
};

function safe(req, res) {
  const tainted = req.query.name;

  res.send(sanitizeHtml(tainted)); // compliant
};
