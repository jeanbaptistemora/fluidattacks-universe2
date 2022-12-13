import { Router } from "express";
import crypto from "crypto";


const router = Router();

router.get("/test139/:target", function (req, res) {
  let target = req.params["target"];
  const hash = crypto.createHash("RSA-MD4");

  hash.on("readable", () => {
    const data = hash.read();
    if (data) {
      res.json({ hash: data.toString("hex") });
    }
  });
  hash.write(target);
  hash.end();
});

export default router
