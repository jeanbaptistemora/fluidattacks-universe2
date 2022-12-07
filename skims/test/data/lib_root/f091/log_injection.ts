import { parse } from "url";
import {Logger, log} from "logging.ts";
import {HttpReq, HttpRes, ReqUrl} from "types.ts";

function unsafe_log(req: HttpReq, res: HttpRes) {
  const q: ReqUrl = parse(req.url, true);

  const userName: string = q.query.username;
  // UNSAFE: Unsanitized user input
  Logger.info(userName);
  log.info(userName);

  // UNSAFE: Incorrectly sanitized user input
  const userName2: string = q.query.username.replace(/\n|\f/g, "");
  console.info(userName2);
}



function safe_log(req: HttpReq, res: HttpRes) {
  const q: ReqUrl = parse(req.url, true);
  const username: string = q.query.username.replace(/\n|\r/g, "");
  // SAFE: Sanitized input from the user
  console.info(username);
}
