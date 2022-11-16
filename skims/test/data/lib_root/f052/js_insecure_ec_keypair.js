import { Router } from "express";
const router = Router();
const { generateKeyPair } = require("crypto");

function test(req, res) {
  generateKeyPair(
    "ec",
    {
      namedCurve: "secp192k1",
      publicKeyEncoding: {
        type: "spki",
        format: "pem",
      },
      privateKeyEncoding: {
        type: "pkcs8",
        format: "pem",
      },
    },
    (err, publicKey, privateKey) => {
      if (err) console.log("Error!", err);
      res.send(publicKey);
    }
  );
}

router.get("/test134", test);

export default router;
