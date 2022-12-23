import { Router } from "express";
import { reqData, resData } from "types.ts";
var router = Router();

router.get("test008", function (req: reqData, res: resData) {
  var user: string = req.params["user"];
  res.setHeader("X-XSS-Protection", "0");
  res.send(`
    <!DOCTYPE html>
    <html>
      <body>
        <h1>Hello ${user}</h1>
      </body>
    </html>
    `
  );
});

export default router;
