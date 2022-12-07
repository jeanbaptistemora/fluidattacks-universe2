//Noncompliant

const execa = require('execa');

async function injection_args(req, res) {
  const cmd = "ls -la "+req.query.arg;

  const {stdout} = await execa.command(cmd);
}

const cp = require('child_process');

function vuln_injection_command(req, res) {
  const cmd = 'ls '+req.query.arg;

  const out = cp.execSync(cmd);
}

//Compliant

function sec_injection_command(req, res) {
  const out = cp.execFileSync("ls", [req.query.arg]); // Compliant
}


async function sec_injection_args(req, res) {
  const arg = req.query.arg;

  const {stdout} = await execa("ls", ["-la", arg]); // Compliant
}
