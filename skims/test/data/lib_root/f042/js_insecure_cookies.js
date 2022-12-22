import { Router } from "express";
var router = Router();

router.get("test042", function (req, res) {

  var secure = false;
  res.cookie("SomeCookie", "Some Value", { secure: secure, httpOnly: true });
  res.send("anything");

});

export default router;
