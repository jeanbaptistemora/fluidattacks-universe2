import { Router } from "express";
var xpath = require("xpath");
let fs = require("fs");
var router = Router();

router.get("/test142/", function (req, res) {

  let userData = req.body;
  let userName = userData.username;
  let password = userData.password;

  fs.readFinding("test", (error, data) => {

    var findUserXPath = `//Employee[UserName/text()='${userName}' and Password/text()='${password}']`;
    let result = xpath.select(findUserXPath, doc);
    return result;

  });

});

export default router;
