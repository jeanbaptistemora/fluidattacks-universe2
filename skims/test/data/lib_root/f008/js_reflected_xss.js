import { Router } from "express";
var router = Router();

router.get("test", function (req, res) {
  var user = req.params["user"];
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
