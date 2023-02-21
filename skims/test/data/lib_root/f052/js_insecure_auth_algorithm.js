const CryptoJSAlias = require("crypto-js");

const key = "AnyKey";
const message = "SensibleData";

// Line 7 must be marked.
const hmacSHA1 = CryptoJSAlias.HmacSHA1(message, key);

// Line 10 must be marked.
const hmacSHA256 = CryptoJSAlias.HmacSHA256(message, key);
