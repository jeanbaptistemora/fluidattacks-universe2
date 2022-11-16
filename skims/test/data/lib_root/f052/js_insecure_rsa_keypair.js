/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import { Router } from "express";

const router = Router();
const { generateKeyPair } = require("crypto");

function test(_req, res) {
  let key_options = {
    modulusLength: 1024,
    publicKeyEncoding: {
      type: "pkcs1",
      format: "pem",
    },
    privateKeyEncoding: {
      type: "pkcs1",
      format: "pem",
      //cipher: "aes-256-cbc", //Optional
      //passphrase: "", //Optional
    },
  };
  generateKeyPair(
    "rsa",
    key_options,
    (err, publicKey, _privateKey) => {
      if (err) console.log("Error!", err);
      res.send(publicKey);
    }
  );
}

router.get("/test130", test);

export default router;
