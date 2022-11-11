import { Router } from "express";
let CryptoJS = require("crypto-js");
let router = Router();

router.get("/test120/:target", function (req, res) {
  const keyString = "*4wQZgn+U2RW_mb=";

  let parameters = req.params;
  let target = parameters["target"];

  let encryptedAES = CryptoJS.AES.encrypt(target, keyString, {
    mode: CryptoJS.mode.CBC,
    padding: CryptoJS.pad.NoPadding,
  }).toString();
  res.json({ encryptedAES: encryptedAES });
  let encryptedDES = CryptoJS.DES.encrypt(target, keyString, {
    mode: CryptoJS.mode.CBC,
    padding: CryptoJS.pad.NoPadding,
  }).toString();
  res.json({ encryptedDES: encryptedDES });
  let encryptedRC4 = CryptoJS.RC4.encrypt(target, keyString, {
    mode: CryptoJS.mode.CBC,
    padding: CryptoJS.pad.NoPadding,
  }).toString();
  res.json({ encryptedRC4: encryptedRC4 });
  let encryptedRSA = CryptoJS.RSA.encrypt(target, keyString, {
    mode: CryptoJS.mode.CBC,
    padding: CryptoJS.pad.NoPadding,
  }).toString();
  res.json({ encryptedRSA: encryptedRSA });
});

export default router;
