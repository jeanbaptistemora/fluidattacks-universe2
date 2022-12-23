import { Router } from "express";
import { reqData, resData } from "types.ts";
var router = Router();

router.get("test042", function (req: reqData, res: resData) {
  var secure: boolean = false;
  res.cookie("SomeCookie", "Some Value", { secure: secure, httpOnly: true });
  res.send("anything");

});

export default router;
