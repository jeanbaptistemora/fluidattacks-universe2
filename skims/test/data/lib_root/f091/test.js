import { createServer } from "http";
import { parse } from "url";

function serverInt(req, res) {
  const q = parse(req.url, true);

  // GOOD: remove newlines from user controlled input before logging
  const username = q.query.username.replace(/\n|\r/g, "");

  console.info(username);
}

const server = createServer(serverInt);

server.listen(3000, "127.0.0.1", () => {});

function badServerInt(req, _res) {
  const q = parse(req.url, true);

  Logger.info(q.query.username); // BAD: User input logged as-
  log.info(q.query.username); // BAD: User input logged as-is
  console.info(q.query.username.replace(/\f|\f/g, ""));
}
const badServer = createServer(badServerInt);

badServer.listen(3000, "127.0.0.1", () => {});
