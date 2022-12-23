import { Router } from "express";
import { xpath } from "xpath";
import { reqData, resData, readData, docFile } from "types.ts";
import { fs } from "fs";


var router = Router();
router.get("test021", function (req: reqData, res: resData) {

  let userData = req.body;
  let userName = userData.username;
  let password = userData.password;

  fs.readFinding("test", (error: Error, data: readData, doc: docFile) => {

    var findUserXPath = `//Employee[UserName/text()='${userName}' and Password/text()='${password}']`;
    let result = xpath.select(findUserXPath, doc);
    return result;

  });

});

export default router;
