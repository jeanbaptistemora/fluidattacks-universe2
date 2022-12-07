import { parse } from "url";

function unsafe_log(req, _res) {
  const q = parse(req.url, true);
  const userName = q.query.username;
  // UNSAFE: Unsanitized user input
  Logger.info(userName);
  log.info(userName);

  // UNSAFE: Incorrectly sanitized user input
  const userName2 = userName.replace(/\f/g, "");
  console.info(userName2);
}



function safe_log(req, res) {
  const q = parse(req.url, true);
  const username = q.query.username.replace(/\n|\r/g, "");
  // SAFE: Sanitized input from the user
  console.info(username);
}
