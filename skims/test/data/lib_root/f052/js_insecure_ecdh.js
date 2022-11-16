import { Router } from "express";
import * as crypto from "crypto";
const router = Router();

router.get("/test127", function (req, res) {
  const bob = crypto.createECDH("c2pnb163v2");
  const bobKey = bob.generateKeys();
  res.send(bobKey.toString("hex"));
});

export default router;
