import { Router } from "express";
import { reqData, resData, dBConnection } from "types.ts";
import { mysql } from "mysql";
var router = Router();
var connection: dBConnection = mysql.createConnection();

router.get("test112", function (req: reqData, res: resData) {

  connection.connect();
  connection.resume();
  let userData = req.body;
  let userName = userData.username;
  let password = userData.password;

  connection.query(
    `SELECT * FROM users WHERE user_name='${userName}' AND password='${password}'`,
    function (err: Error) { res.send(err); }
  );
});

export default router;
