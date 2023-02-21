const hmacSHA1 = require("crypto-js/hmac-sha1");
const hmacSHA256 = require("crypto-js/hmac-sha256");

const key = "AnyKey";
const message = "SensibleData";

// Lines 8 and 9 should be marked
const hmacSHA1Result = hmacSHA1(message, key);
const hmacSHA256Result = hmacSHA256(message, key);
