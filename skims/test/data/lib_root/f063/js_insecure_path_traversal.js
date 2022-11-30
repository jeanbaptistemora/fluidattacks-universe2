const fs = require("fs");
const pathmodule = require("path");

function unsafeCases(req, res) {

  const reqPath = req.query.filename; // user-controlled path
  let data = fs.readFileSync(reqPath, { encoding: "utf8", flag: "r" }); // Noncompliant

}

function safeCases(req, res) {

  let safedata = fs.readFileSync("./dir/downloads", { encoding: "utf8", flag: "r" });

  const reqPath = req.query.filename;
  const resolvedPath = pathmodule.resolve(reqPath); // resolve will sanitize the input
  if (resolvedPath.startsWith(__dirname + '/uploads')) { // ensures a whitelist verification
    let data = fs.readFileSync(resolvedPath, { encoding: 'utf8', flag: 'r' }); // Compliant
  }
}
