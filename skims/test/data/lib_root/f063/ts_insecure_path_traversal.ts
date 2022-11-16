/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import fs from "fs";
import pathmodule from "path";

function safePathInjection(req, res) {
  const reqPath = __dirname + req.query.filename; // user-controlled path
  const resolvedPath = pathmodule.resolve(reqPath); // resolve will resolve "../"

  if (resolvedPath.startsWith(__dirname + "/uploads")) {
    // the requested filename cannot be retrieved outside of the "/uploads" folder
    let data = fs.readFileSync(resolvedPath, { encoding: "utf8", flag: "r" }); // Compliant
  }
}

function unsafePathInjection(req, res) {
  const reqPath = __dirname + req.query.filename; // user-controlled path

  let data = fs.readFileSync(reqPath, { encoding: "utf8", flag: "r" }); // Noncompliant
}
