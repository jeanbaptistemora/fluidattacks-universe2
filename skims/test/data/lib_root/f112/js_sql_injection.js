import { Router } from "express";
var router = Router();
var mysql = require("mysql");
var connection = mysql.createConnection();

router.get("test112", function (req, res) {

  connection.connect();
  connection.resume();
  let userData = req.body;
  let userName = userData.username;
  let password = userData.password;

  connection.query(
    `SELECT * FROM users WHERE user_name='${userName}' AND password='${password}'`,
    function (error, results, fields) {res.json({ ok: results.length > 0 });}
  );
});

export default router;
