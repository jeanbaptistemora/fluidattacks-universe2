import { Router } from "express";
var router = Router();

router.get("test", function (req, res) {
  var user = req.params["user"];
  exec("ls target/user_files/" + user + "/", (error, stdout, stderr) => {
    res.json(data);
  });
});

export default router;
